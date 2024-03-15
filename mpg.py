#!/usr/bin/env python3
#
#

import time
import serial
import hal
from struct import pack, unpack

# setup
device = "/dev/ttyACM0"
baud = 115200

RX_SIZE = 32
AXIS = ("x", "y", "z", "a", "b", "c")
OVERWRITES = ("feed", "rapid" , "spindle")
BUTTON_NAMES = ("01", "02", "03", "04", "05", "06", "01b", "enc01", "enc02", "enc03", "estop", "06b")


# create hal pins
h = hal.component("mpg")
for axis in AXIS:
    h.newpin(f"axis.{axis}.pos", hal.HAL_FLOAT, hal.HAL_IN)
    h.newpin(f"axis.{axis}.jog-counts", hal.HAL_S32, hal.HAL_OUT)
for name in OVERWRITES:
    h.newpin(f"override.{name}.value", hal.HAL_FLOAT, hal.HAL_IN)
    h.newpin(f"override.{name}.counts", hal.HAL_S32, hal.HAL_OUT)
for name in BUTTON_NAMES:
    h.newpin(f"button.{name}", hal.HAL_BIT, hal.HAL_OUT)
    h.newpin(f"button.{name}-not", hal.HAL_BIT, hal.HAL_OUT)
h.ready()


# init serial
ser = serial.Serial(device, baud, timeout=0.01)
while ser.inWaiting() > 0:
    ser.read(1)


# main loop
while True:

    # pack and send tx data
    data = b''
    for axis in AXIS:
        data += pack("<f", h[f"axis.{axis}.pos"])
    for name in OVERWRITES:
        data += pack("<h", int(h[f"override.{name}.value"] * 100.0))
    ser.write(bytes(data))

    # receive and unpack rx data
    msgFromServer = ser.read(RX_SIZE)
    if msgFromServer and len(msgFromServer) == RX_SIZE:
        bpos = 0
        for axis in AXIS:
            h[f"axis.{axis}.jog-counts"] = unpack("<i", bytes(msgFromServer[bpos:bpos+4]))[0]
            bpos += 4
        for name in OVERWRITES:
            h[f"override.{name}.counts"] = unpack("<h", bytes(msgFromServer[bpos:bpos+2]))[0]
            bpos += 2
        buttons = unpack("<H", bytes(msgFromServer[bpos:bpos+2]))[0]
        bpos += 2
        for num, name in enumerate(BUTTON_NAMES):
            if buttons & (1<<num) == 0:
                h[f"button.{name}"] = False
            else:
                h[f"button.{name}"] = True
            h[f"button.{name}-not"] = not h[f"button.{name}"]

    # serial sync
    while ser.inWaiting() > 0:
        ser.read(1)

    #time.sleep(0.01)

