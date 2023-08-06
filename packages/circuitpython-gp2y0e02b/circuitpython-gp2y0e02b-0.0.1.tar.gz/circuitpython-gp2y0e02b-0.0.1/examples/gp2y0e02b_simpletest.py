# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: Unlicense

import time
import board
import gpy


i2c = board.I2C()  # uses board.SCL and board.SDA

# Initialize the MPL3115A2.
gpy = gpy.GP2Y0E02B(i2c)

while True:
    gpy.read_distance()
    time.sleep(0.2)
