# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`gp2y0e02b`
================================================================================

Driver for the GP2Y0E02B distance sensor


* Author(s): Jose D. Montoya

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads


* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register

"""

from micropython import const
from adafruit_bus_device import i2c_device
from adafruit_register.i2c_struct import UnaryStruct

try:
    from busio import I2C
except ImportError:
    pass


__version__ = "0.0.1"
__repo__ = "https://github.com/jposada202020/CircuitPython_GP2Y0E02B.git"

_I2C_ADDR = const(0x40)

# pylint: disable= invalid-name, too-many-instance-attributes, missing-function-docstring
# pylint: disable=too-few-public-methods


class GP2Y0E02B:
    """Driver for the GP2Y0E02B Sensor connected over I2C.

    :param ~busio.I2C i2c_bus: The I2C bus the GP2Y0E02B is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x40`

    :raises RuntimeError: if the sensor is not found

    **Quickstart: Importing and using the device**

    Here is an example of using the :class:`GP2Y0E02B` class.
    First you will need to import the libraries to use the sensor

    .. code-block:: python

        import board
        import gp2y0e02b as GP2Y0E02B

    Once this is done you can define your `board.I2C` object and define your sensor object

    .. code-block:: python

        i2c = board.I2C()  # Uses board.SCL and board.SDA
        gpy = GP2Y0E02B.GP2Y0E02B(i2c)

    Now you have access to the attributes

    .. code-block:: python

        distance = gpy.distance

    """

    _write_address = UnaryStruct(0x80, "B")
    _read_address = UnaryStruct(0x81, "H")

    _distance_MSB = UnaryStruct(0x5F, "H")
    _distance_LSB = UnaryStruct(0x5E, "B")
    _n_value = UnaryStruct(0x35, "B")
    _suspend_mode = UnaryStruct(0xE8, "B")

    def __init__(self, i2c_bus: I2C, address: int = _I2C_ADDR) -> None:
        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)

    @property
    def distance(self) -> float:
        high = self._distance_MSB & 0x7F8
        low = self._distance_LSB & 0x07
        total = (high | low) / 16 / 2**self._n_value
        return total
