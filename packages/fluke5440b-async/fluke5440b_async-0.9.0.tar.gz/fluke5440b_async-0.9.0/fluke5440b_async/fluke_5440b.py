# ##### BEGIN GPL LICENSE BLOCK #####
#
# Copyright (C) 2023 Patrick Baus
# This file is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####
from __future__ import annotations

import asyncio
import logging
from decimal import Decimal
from typing import TYPE_CHECKING, cast

from fluke5440b_async.enums import DeviceState, ErrorCode, ModeType, SeparatorType, TerminatorType
from fluke5440b_async.errors import DeviceError, SelftestError
from fluke5440b_async.flags import SerialPollFlags, SrqMask, StatusFlags

if TYPE_CHECKING:
    from async_gpib import AsyncGpib
    from prologix_gpib_async import AsyncPrologixGpibController

BAUD_RATES_AVAILABLE = (50, 75, 110, 134.5, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600)


class Fluke_5440B:  # noqa pylint: disable=too-many-public-methods,invalid-name
    @property
    def connection(self) -> AsyncGpib | AsyncPrologixGpibController:
        """
        The GPIB connection.
        """
        return self.__conn

    def __init__(self, connection: AsyncGpib | AsyncPrologixGpibController):
        self.__conn = connection
        self.__lock: asyncio.Lock | None = None

        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(logging.WARNING)  # Only log really important messages by default

    async def get_id(self) -> tuple[str, str, str, str]:
        version = (await self._get_software_version()).strip()
        return "Fluke", "5440B", version, "0"

    def set_log_level(self, loglevel: int = logging.WARNING):
        self.__logger.setLevel(loglevel)

    async def connect(self) -> None:
        self.__lock = asyncio.Lock()

        await self.__conn.connect()
        if hasattr(self.__conn, "set_eot"):
            # Used by the Prologix adapters
            await self.__conn.set_eot(False)

        async with self.__lock:
            status = await self.serial_poll()  # clears the SRQ bit
            while status & SerialPollFlags.MSG_RDY:  # clear message buffer
                msg = await self.read()
                self.__logger.debug("Calibrator message at boot: %s.", msg)
                status = await self.serial_poll()

            if status & SerialPollFlags.ERROR_CONDITION:
                err = await self.get_error()  # clear error flags not produced by us
                self.__logger.debug("Calibrator errors at boot: %s.", err)
            state = await self.get_state()
            self.__logger.debug("Calibrator state at boot: %s.", state)
            if state != DeviceState.IDLE:
                await self.set_srq_mask(SrqMask.DOING_STATE_CHANGE)
                await self.__wait_for_idle()

            await self.__set_terminator(TerminatorType.LF_EOI)  # terminate lines with \n
            await self.__set_separator(SeparatorType.COMMA)  # use a comma as the separator
            await self.set_srq_mask(SrqMask.NONE)  # Disable interrupts

    async def disconnect(self) -> None:
        try:
            # Return access to the device
            await self.local()
        except ConnectionError:
            pass
        finally:
            await self.__conn.disconnect()

    async def write(self, cmd: str | bytes, test_error: bool = False):
        assert isinstance(cmd, (str, bytes))
        try:
            cmd = cmd.encode("ascii")  # type: ignore[union-attr]
        except AttributeError:
            pass  # cmd is already a bytestring
        assert isinstance(cmd, bytes)
        # The calibrator can only buffer 127 byte
        if len(cmd) > 127:
            raise ValueError("Command size must be 127 byte or less.")

        await self.__conn.write(cmd)
        if test_error:
            await asyncio.sleep(0.2)  # The instrument is slow in parsing commands
            spoll = await self.serial_poll()
            if spoll & SerialPollFlags.ERROR_CONDITION:
                msg = None
                if spoll & SerialPollFlags.MSG_RDY:
                    # The command did return some msg, so we need to read that first (and drop it)
                    msg = await self.read()

                err = await self.get_error()
                if msg is None:
                    raise DeviceError(f"Device error on command: {cmd.decode('utf-8')}, code: {err}", err)
                raise DeviceError(
                    f"Device error on command: {cmd.decode('utf-8')}, code: {err}, Message returned: {msg}", err
                )

    async def read(self) -> str | list[str]:
        result = (await self.__conn.read()).rstrip().decode("utf-8").split(",")  # strip \n and split at the separator
        return result[0] if len(result) == 1 else result

    async def query(self, cmd: str | bytes, test_error: bool = False) -> str | list[str]:
        await self.write(cmd, test_error)
        return await self.read()

    async def __wait_for_state_change(self) -> None:
        while (await self.serial_poll()) & SerialPollFlags.DOING_STATE_CHANGE:
            await asyncio.sleep(0.5)

    async def reset(self) -> None:
        assert self.__lock is not None
        async with self.__lock:
            # We do not send "RESET", because a DCL will do the same and additionally circumvents the input buffer
            await self.__conn.clear()
            # We cannot use interrupts, because the device is resetting all settings and will not accept commands
            # until it has reset. So we will poll the status register first, and when this is done, we will poll
            # the device itself until it is ready
            await self.__wait_for_state_change()
            while (await self.get_state()) != DeviceState.IDLE:
                await asyncio.sleep(0.5)

            await self.__set_terminator(TerminatorType.LF_EOI)  # terminate lines with \n
            await self.__set_separator(SeparatorType.COMMA)  # use a comma as the separator
            await self.set_srq_mask(SrqMask.NONE)  # Disable interrupts

    async def local(self) -> None:
        await self.__conn.ibloc()

    async def get_terminator(self) -> TerminatorType:
        assert self.__lock is not None
        async with self.__lock:
            result = await self.query("GTRM", test_error=True)
            try:
                assert isinstance(result, str)
                term = int(result)
            except TypeError:
                raise TypeError(f"Invalid reply received. Expected an integer, but received: {result}") from None
            return TerminatorType(term)

    async def __set_terminator(self, value: TerminatorType) -> None:
        """
        Engage lock, before calling
        """
        assert isinstance(value, TerminatorType)
        await self.write(f"STRM {value.value:d}", test_error=True)
        await self.__wait_for_state_change()

    async def get_separator(self) -> SeparatorType:
        result = await self.query("GSEP", test_error=True)
        try:
            assert isinstance(result, str)
            sep = int(result)
        except TypeError:
            raise TypeError(f"Invalid reply received. Expected an integer, but received: {result}") from None
        return SeparatorType(sep)

    async def __set_separator(self, value: SeparatorType) -> None:
        """
        Engage lock, before calling
        """
        assert isinstance(value, SeparatorType)
        await self.write(f"SSEP {value.value:d}", test_error=True)
        await self.__wait_for_state_change()

    async def set_mode(self, value: ModeType) -> None:
        assert isinstance(value, ModeType)
        await self.write(f"{value.value}", test_error=True)

    async def set_output_enabled(self, enabled: bool) -> None:
        await self.write("OPER" if enabled else "STBY", test_error=True)

    async def get_output(self) -> Decimal:
        result = await self.query("GOUT", test_error=True)
        assert isinstance(result, str)
        return Decimal(result)

    def __limit_numeric(self, value: int | float | Decimal) -> str:
        # According to page 4-5 of the operator manual, the value needs to meet the following criteria:
        # - Maximum of 8 significant digits
        # - Exponent must have less than two digits
        # - Integers must be less than 256
        # - 10e-12 < abs(value) < 10e8
        # Limit to to 10*-8 resolution (10 nV is the minimum)
        result = f"{value:.8f}"
        if abs(value) >= 1:  # type: ignore[operator]
            # There are significant digits before the decimal point, so we need to limit the length of the string
            # to 9 characters (decimal point + 8 significant digits)
            result = f"{result:.9s}"
        return result

    async def set_output(self, value: int | float | Decimal, test_error: bool = True) -> None:
        if -1500 > value > 1500:
            raise ValueError("Value out of range")
        try:
            await self.write(f"SOUT {self.__limit_numeric(value)}", test_error)
        except DeviceError as e:
            if e.code == ErrorCode.OUTPUT_OUTSIDE_LIMITS:
                raise ValueError("Value out of range") from None
            raise

    async def set_internal_sense(self, enabled: bool) -> None:
        try:
            await self.write("ISNS" if enabled else "ESNS", test_error=True)
        except DeviceError as e:
            if e.code == ErrorCode.INVALID_SENSE_MODE:
                raise TypeError("Sense mode not allowed.") from None
            raise

    async def set_internal_guard(self, enabled: bool) -> None:
        try:
            await self.write("IGRD" if enabled else "EGRD", test_error=True)
        except DeviceError as e:
            if e.code == ErrorCode.INVALID_GUARD_MODE:
                raise TypeError("Guard mode not allowed.") from None
            raise

    async def set_divider(self, enabled: bool) -> None:
        await self.write("DIVY" if enabled else "DIVN", test_error=True)

    async def get_voltage_limit(self) -> tuple[Decimal, Decimal]:
        # TODO: Needs testing for error when in current boost mode
        result = await self.query("GVLM", test_error=True)
        return Decimal(result[1]), Decimal(result[0])

    async def set_voltage_limit(
        self, value: int | float | Decimal, value2: int | float | Decimal | None = None
    ) -> None:
        value = Decimal(value)
        if -1500 > value > 1500:
            raise ValueError("Value out of range.")
        if value2 is not None:
            value2 = Decimal(value2)
            if not -1500 <= value2 <= 1500:
                raise ValueError("Value out of range.")
            if not value * value2 <= 0:
                # Make sure, that one value is positive and one value negative or zero.
                raise ValueError("Invalid voltage limit.")

        try:
            if value2 is not None:
                await self.write(f"SVLM {self.__limit_numeric(value2)}", test_error=True)
            await self.write(f"SVLM {self.__limit_numeric(value)}", test_error=True)
        except DeviceError as e:
            if e.code == ErrorCode.LIMIT_OUT_OF_RANGE:
                raise ValueError("Invalid voltage limit.") from None
            raise

    async def get_current_limit(self) -> Decimal | tuple[Decimal, Decimal]:
        # TODO: Needs testing for error when in voltage boost mode
        result = await self.query("GCLM", test_error=True)
        if isinstance(result, list):
            return Decimal(result[1]), Decimal(result[0])
        return Decimal(result)

    async def set_current_limit(
        self, value: int | float | Decimal, value2: int | float | Decimal | None = None
    ) -> None:
        value = Decimal(value)
        if -20 > value > 20:
            raise ValueError("Value out of range.")
        if value2 is not None:
            value2 = Decimal(value2)
            if not -20 <= value2 <= 20:
                raise ValueError("Value out of range.")
            if not value * value2 <= 0:
                raise ValueError("Invalid current limit.")

        try:
            if value2 is not None:
                await self.write(f"SCLM {self.__limit_numeric(value2)}", test_error=True)
            await self.write(f"SCLM {self.__limit_numeric(value)}", test_error=True)
        except DeviceError as e:
            if e.code == ErrorCode.LIMIT_OUT_OF_RANGE:
                raise ValueError("Invalid current limit.") from None
            raise

    async def _get_software_version(self) -> str:
        result = await self.query("GVRS", test_error=True)
        assert isinstance(result, str)
        return result

    async def get_status(self) -> StatusFlags:
        result = await self.query("GSTS", test_error=True)
        try:
            assert isinstance(result, str)
            status = int(result)
        except TypeError:
            raise TypeError(f"Invalid reply received. Expected an integer, but received: {result}") from None

        return StatusFlags(status)

    async def get_error(self) -> ErrorCode:
        result = await self.query("GERR", test_error=True)
        try:
            assert isinstance(result, str)
            error_code = int(result)
        except TypeError:
            raise TypeError(f"Invalid reply received. Expected an integer, but received: {result}") from None

        return ErrorCode(error_code)

    async def get_state(self) -> DeviceState:
        result = await self.query("GDNG", test_error=True)
        try:
            assert isinstance(result, str)
            dev_state = int(result)
        except TypeError:
            raise TypeError(f"Invalid reply received. Expected an integer, but received: {result}") from None

        return DeviceState(dev_state)

    async def __wait_for_rqs(self) -> None:
        try:
            await self.__conn.wait((1 << 11) | (1 << 14))  # Wait for RQS or TIMO
        except asyncio.TimeoutError:
            self.__logger.warning(
                "Timeout during wait. Is the IbaAUTOPOLL(0x7) bit set for the board? Or the timeout set too low?"
            )

        spoll = await self.serial_poll()  # Clear the SRQ bit
        if spoll & SerialPollFlags.ERROR_CONDITION:
            # If there was an error during waiting, raise it.
            # I have seen GPIB_HANDSHAKE_ERRORs with a prologix adapter, which does a lot of polling during wait.
            # Ignore that error for now.
            err = await self.get_error()
            if err is ErrorCode.GPIB_HANDSHAKE_ERROR:
                self.__logger.info(
                    "Got error during waiting: %s. "
                    "If you are using a Prologix adapter, this can be safely ignored at this point.",
                    err,
                )
            else:
                raise DeviceError(f"Device error, code: {err}", err)

    async def __wait_for_idle(self) -> None:
        """
        Make sure, that SrqMask.DOING_STATE_CHANGE is set.
        """
        state = await self.get_state()
        while state != DeviceState.IDLE:
            self.__logger.info("Calibrator busy: %s.", state)
            await self.__wait_for_rqs()
            state = await self.get_state()

    async def selftest_digital(self) -> None:
        assert self.__lock is not None
        async with self.__lock:
            await self.set_srq_mask(SrqMask.DOING_STATE_CHANGE)  # Enable SRQs to wait for each test step
            try:
                self.__logger.info("Running digital self-test. This takes about 5 seconds.")
                await self.__wait_for_idle()

                await self.write("TSTD", test_error=True)
                while "testing":
                    await self.__wait_for_rqs()
                    status = await self.serial_poll()
                    if status & SerialPollFlags.MSG_RDY:
                        msg = await self.read()
                        self.__logger.warning("Digital self-test failed with message: %s.", msg)
                        raise SelftestError(f"Digital self-test failed with message: {msg}.", msg)
                    if status & SerialPollFlags.DOING_STATE_CHANGE:
                        state = await self.get_state()
                        if state not in (
                            DeviceState.IDLE,
                            DeviceState.SELF_TEST_MAIN_CPU,
                            DeviceState.SELF_TEST_FRONTPANEL_CPU,
                            DeviceState.SELF_TEST_GUARD_CPU,
                        ):
                            self.__logger.warning("Digital self-test failed. Invalid state: %s.", state)

                        if state == DeviceState.IDLE:
                            break
                        self.__logger.info("Self-test status: %s.", state)
                self.__logger.info("Digital self-test passed.")
            finally:
                await self.set_srq_mask(SrqMask.NONE)  # Disable SRQs

    async def selftest_analog(self) -> None:
        assert self.__lock is not None
        async with self.__lock:
            await self.set_srq_mask(SrqMask.DOING_STATE_CHANGE)  # Enable SRQs to wait for each test step
            try:
                self.__logger.info("Running analog self-test. This takes about 4 minutes.")
                await self.__wait_for_idle()

                await self.write("TSTA", test_error=True)
                while "testing":
                    await self.__wait_for_rqs()
                    status = await self.serial_poll()
                    if status & SerialPollFlags.MSG_RDY:
                        msg = await self.read()
                        self.__logger.warning("Analog self-test failed with message: %s.", msg)
                        raise SelftestError(f"Analog self-test failed with message: {msg}.", msg)
                    if status & SerialPollFlags.DOING_STATE_CHANGE:
                        state = await self.get_state()
                        if state not in (
                            DeviceState.IDLE,
                            DeviceState.CALIBRATING_ADC,
                            DeviceState.SELF_TEST_LOW_VOLTAGE,
                            DeviceState.SELF_TEST_OVEN,
                        ):
                            self.__logger.warning("Analog self-test failed. Invalid state: %s.", state)

                        if state == DeviceState.IDLE:
                            break
                        self.__logger.info("Self-test status: %s.", state)
                self.__logger.info("Analog self-test passed.")
            finally:
                await self.set_srq_mask(SrqMask.NONE)  # Disable SRQs

    async def selftest_hv(self) -> None:
        assert self.__lock is not None
        async with self.__lock:
            await self.set_srq_mask(SrqMask.DOING_STATE_CHANGE)  # Enable SRQs to wait for each test step
            try:
                self.__logger.info("Running high voltage self-test. This takes about 1 minute.")
                await self.__wait_for_idle()

                await self.write("TSTH", test_error=True)
                while "testing":
                    await self.__wait_for_rqs()
                    status = await self.serial_poll()
                    if status & SerialPollFlags.MSG_RDY:
                        msg = await self.read()
                        self.__logger.warning("High voltage self-test failed with message: %s.", msg)
                        raise SelftestError(f"High voltage self-test failed with message: {msg}.", msg)
                    if status & SerialPollFlags.DOING_STATE_CHANGE:
                        state = await self.get_state()
                        if state not in (
                            DeviceState.IDLE,
                            DeviceState.CALIBRATING_ADC,
                            DeviceState.SELF_TEST_HIGH_VOLTAGE,
                        ):
                            self.__logger.warning("High voltage self-test failed. Invalid state: %s.", state)

                        if state == DeviceState.IDLE:
                            break
                        self.__logger.info("Self-test status: %s.", state)
                self.__logger.info("High voltage self-test passed.")
            finally:
                await self.set_srq_mask(SrqMask.NONE)  # Disable SRQs

    async def selftest_all(self) -> None:
        await self.selftest_digital()
        await self.selftest_analog()
        await self.selftest_hv()

    async def acal(self) -> None:
        assert self.__lock is not None
        async with self.__lock:
            await self.set_srq_mask(SrqMask.DOING_STATE_CHANGE)  # Enable SRQs to wait for each calibration step
            try:
                self.__logger.info("Running internal calibration. This will take about 6.5 minutes.")
                await self.__wait_for_idle()

                await self.write("CALI", test_error=True)
                while "calibrating":
                    await self.__wait_for_rqs()
                    await self.serial_poll()
                    state = await self.get_state()
                    if state not in (
                        DeviceState.IDLE,
                        DeviceState.CALIBRATING_ADC,
                        DeviceState.ZEROING_10V_POS,
                        DeviceState.CAL_N1_N2_RATIO,
                        DeviceState.ZEROING_10V_NEG,
                        DeviceState.ZEROING_20V_POS,
                        DeviceState.ZEROING_20V_NEG,
                        DeviceState.ZEROING_250V_POS,
                        DeviceState.ZEROING_250V_NEG,
                        DeviceState.ZEROING_1000V_POS,
                        DeviceState.ZEROING_1000V_NEG,
                        DeviceState.CALIBRATING_GAIN_10V_POS,
                        DeviceState.CALIBRATING_GAIN_20V_POS,
                        DeviceState.CALIBRATING_GAIN_HV_POS,
                        DeviceState.CALIBRATING_GAIN_HV_NEG,
                        DeviceState.CALIBRATING_GAIN_20V_NEG,
                        DeviceState.CALIBRATING_GAIN_10V_NEG,
                        DeviceState.WRITING_TO_NVRAM,
                    ):
                        self.__logger.warning("Internal calibration failed. Invalid state: %s.", state)

                    if state == DeviceState.IDLE:
                        break
                    self.__logger.info("Calibration status: %s", state)
                self.__logger.info("Internal calibration done.")
            finally:
                await self.set_srq_mask(SrqMask.NONE)  # Disable SRQs

    async def get_calibration_constants(self) -> dict[str, Decimal]:
        assert self.__lock is not None
        async with self.__lock:
            # We need to split the query in two parts, because the input buffer of the 5440B is only 127 byte
            values = cast(list[str], await self.query(",".join(["GCAL " + str(i) for i in range(10)]), test_error=True))
            values += cast(
                list[str], await self.query(",".join(["GCAL " + str(i) for i in range(10, 20)]), test_error=True)
            )
            return {
                "gain_0.2V": Decimal(values[5]),
                "gain_2V": Decimal(values[4]),
                "gain_10V": Decimal(values[0]),
                "gain_20V": Decimal(values[1]),
                "gain_250V": Decimal(values[2]),
                "gain_1000V": Decimal(values[3]),
                "offset_10V_pos": Decimal(values[6]),
                "offset_20V_pos": Decimal(values[7]),
                "offset_250V_pos": Decimal(values[8]),
                "offset_1000V_pos": Decimal(values[9]),
                "offset_10V_neg": Decimal(values[10]),
                "offset_20V_neg": Decimal(values[11]),
                "offset_250V_neg": Decimal(values[12]),
                "offset_1000V_neg": Decimal(values[13]),
                "gain_shift_10V": Decimal(values[14]),
                "gain_shift_20V": Decimal(values[15]),
                "gain_shift_250V": Decimal(values[16]),
                "gain_shift_1000V": Decimal(values[17]),
                "resolution_ratio": Decimal(values[18]),
                "adc_gain": Decimal(values[19]),
            }

    async def get_rs232_baud_rate(self) -> int | float:
        result = await self.query("GBDR", test_error=True)
        try:
            assert isinstance(result, str)
            baud_rate = int(result)
        except TypeError:
            raise TypeError(f"Invalid reply received. Expected an integer, but received: {result}") from None
        return BAUD_RATES_AVAILABLE[baud_rate]

    async def set_rs232_baud_rate(self, value: int | float) -> None:
        if value not in BAUD_RATES_AVAILABLE:
            raise ValueError(f"Invalid baud rate. It must be one of: {','.join(map(str, BAUD_RATES_AVAILABLE))}.")
        assert self.__lock is not None
        async with self.__lock:
            self.__logger.info("Setting baud rate and writing to NVRAM. This takes about 1.5 minutes.")
            try:
                await self.write(f"SBDR {BAUD_RATES_AVAILABLE.index(value):d}", test_error=True)
                await self.set_srq_mask(SrqMask.DOING_STATE_CHANGE)  # Enable SRQs to wait until written to NVRAM
                await asyncio.sleep(0.5)
                await self.__wait_for_idle()
            finally:
                await self.set_srq_mask(SrqMask.NONE)  # Disable SRQs

    async def set_enable_rs232(self, enabled: bool) -> None:
        await self.write("MONY" if enabled else "MONN", test_error=True)

    async def serial_poll(self) -> SerialPollFlags:
        return SerialPollFlags(int(await self.__conn.serial_poll()))

    async def get_srq_mask(self) -> SrqMask:
        result = await self.query("GSRQ", test_error=True)
        try:
            assert isinstance(result, str)
            mask = int(result)
        except TypeError:
            raise TypeError(f"Invalid reply received. Expected an integer, but received: {result}") from None
        return SrqMask(mask)

    async def set_srq_mask(self, value: SrqMask) -> None:
        assert isinstance(value, SrqMask)
        await self.write(f"SSRQ {value.value:d}", test_error=True)
