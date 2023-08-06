#!/usr/bin/env python3
"""A utility class to leverage 74HC595 shift register chips with a Raspberry Pi."""

# Core Library modules
import time
from typing import Union

# Third party modules
import RPi.GPIO as GPIO

# GPIO Mode: BOARD - Ue raspberry Pi Board pin numbers
#            BCM   - Use Broadcom GPIO pin numbers

GPIO.setwarnings(False)


class HC595:
    def __init__(
        self,
        mode: str = "BCM",
        data: int = 17,
        clock: int = 27,
        latch: int = 18,
        ics: int = 1,
    ):
        """Initialization method to create an instance with the specified mode, the
        three pins being use and the number of 74HC595 being used (daisey-chained).

        Parameters
        ----------
        mode: str
            used to communicate to the RPi library how the pins are being referenced.
        data: int
            Pin being used for data
        clock: int
            Pin being used for clocking information
         latch: int
            Pin being used for latching information

        Example
        --------
        >>> shifter = HC595(mode="BCM", data=17, clock=27, latch=18, ics=2)
        """
        self._DATA = data
        self._CLOCK = clock
        self._LATCH = latch
        if len({self._DATA, self._LATCH, self._CLOCK}) != 3:
            raise Exception("Pins must be Unique")

        self._ICS = ics
        self._mode = mode
        self._current_storage_register = 0
        self._mask = 0x80 << (8 * (self._ICS - 1))
        self._bits = self._ICS * 8
        if self._mode == "BCM":
            GPIO.setmode(GPIO.BCM)
        else:
            GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self._DATA, GPIO.OUT)
        GPIO.setup(self._CLOCK, GPIO.OUT)
        GPIO.setup(self._LATCH, GPIO.OUT)
        GPIO.output(self._DATA, GPIO.LOW)
        GPIO.output(self._CLOCK, GPIO.LOW)
        GPIO.output(self._LATCH, GPIO.LOW)

    def _shift_register(self, value: int) -> None:
        """A private method that fills the shift register with the 'bit pattern' of
        the value.

        Parameters
        ----------
        value: int
            The value to be converted to a bit pattern
            e.g. 16 will get converted to 00010000

        Returns
        -------
        None

        Example
        --------
        >>> _shift_register(16)
        """
        for bit in range(self._bits):
            data_bit = self._mask & (value << bit)
            GPIO.output(self._DATA, data_bit)
            GPIO.output(self._CLOCK, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(self._CLOCK, GPIO.LOW)

    def _storage_register(self) -> None:
        """A private method that will copy the contents of the shift register to the
        storage register.  Once the shift register contains the bit pattern you want
        this method essentially "activates" the output pins.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Examples
        --------
        >>> _storage_register()
        """
        GPIO.output(self._LATCH, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(self._LATCH, GPIO.LOW)

    def clear(self) -> None:
        """A public method to turn the output from the output pins off.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Examples
        --------
        >>> shifter.clear()
        """
        self._shift_register(0)
        self._storage_register()
        self._current_storage_register = 0

    def test(self, repeat: int = 1, speed: str = "medium") -> None:
        """A public method to turn the output from each output pin on then off.
        Once every pin has been turned on and off this can be then repeated any number
         of times and at one of three speeds.

        Parameters
        ----------
        repeat: int
            The number of times to repeat the process
        speed: str
            The speed of the process. Can be either "slow", "medium" or "fast"

        Returns
        -------
        None

        Examples
        --------
        >>> shifter.test(repeat=3, speed="medium")
        """
        pause: Union[int, float]
        if speed not in ["slow", "medium", "fast"]:
            speed = "medium"
        if speed == "slow":
            pause = 1
        elif speed == "medium":
            pause = 0.1
        else:
            pause = 0.01
        try:
            for _ in range(repeat):
                for i in range(self._ICS * 8):
                    self._shift_register(2**i)
                    self._storage_register()
                    time.sleep(pause)
        except KeyboardInterrupt:
            pass

        self._shift_register(self._current_storage_register)
        self._storage_register()

    def set_output(self, output: int, mask: int) -> None:
        """A public method that takes into account the existing settings of the storage
        register, the new values of only the pins we want and the mask to apply. The new
        output value is caluculated

        Parameters
        ----------
        output: int
            value converted to a bit pattern is the pins we want to turn on.
            The output value should be equal to or less than the mask value
        mask: int
            value converted to a bit pattern is the pins we want to change in total.
            If the bits when the mask and output are 0 then the pins are turn off.
            All other pins will stay the same

        Returns
        -------
        None

        Raises
        ------
        ValueError:
            When the bit pattern of the Output Value exceeds physical ouput pins.
            When Output > Mask

        Examples
        --------
        >>> shifter.set_output(8, 12)
        """
        if output.bit_length() > self._bits or mask.bit_length() > self._bits:
            raise ValueError(f"Value is out of range of {self._bits} bits")

        if output > mask:
            raise ValueError("Output Value Exceeds Mask Value")

        self._current_storage_register = (
            self._current_storage_register - (self._current_storage_register & mask)
        ) + output
        self._shift_register(self._current_storage_register)
        self._storage_register()

    def set_pattern(self, chip_pattern: list) -> None:
        """Public method to accept a bit pattern to represent the pins you want to
        turn on.  It does not accept a mask so all output pins will be changed.

        Parameters
        ----------
        chip_pattern: list or list of lists
            The bit pattern to specify which pins are on and off

        Returns
        -------
        None

        Raises
        ------
        ValueError:
            When length of each individual list <> 8
            when length of list of lists <> number of 595 chips

        Examples
        --------
        >>> shifter.set_pattern([0, 0, 1, 1, 0, 0, 0, 0])
        >>> shifter.set_pattern([[0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]])
        """
        dec_repr: int = 0
        mask: int = (2**self._bits) - 1

        if all(isinstance(element, int) for element in chip_pattern):
            if len(chip_pattern) != self._bits:
                raise ValueError("Length of Pattern is incorrect")
            led_pattern = chip_pattern
        elif all(isinstance(element, list) for element in chip_pattern):
            if len(chip_pattern) != self._ICS:
                raise ValueError("Length of Pattern is incorrect")
            led_pattern = [led for chip in chip_pattern for led in chip]
        else:
            raise ValueError("The pattern in incorrectly formatted")

        for bit in range(self._bits):
            dec_repr += led_pattern[bit] * (2**bit)

        self.set_output(dec_repr, mask)
