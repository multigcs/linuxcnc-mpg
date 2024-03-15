#!/usr/bin/env python3
#
#

import os.path
import argparse
import time
import serial
from struct import pack, unpack

# arguments
parser = argparse.ArgumentParser()
parser.add_argument("--device", "-d", help="device", type=str, default="/dev/ttyACM0")
parser.add_argument("--baud", "-b", help="baudrate", type=int, default=115200)
parser.add_argument("--test", "-t", help="test mode / no hal needed", default=False, action="store_true")
parser.add_argument("--scaler", "-s", help="scale selctor", default=False, action="store_true")
parser.add_argument("--leds", "-l", help="disable axis selection / led control by hal", default=False, action="store_true")
args = parser.parse_args()

# setup
RX_SIZE = 12
LONG_PRESS = 20
AXIS = ("x", "y", "z", "a", "b", "c")
OVERWRITES = ("feed", "rapid", "spindle")
LED_NAMES = ("01", "02", "03", "04", "05", "06")
BUTTON_NAMES = (
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "sel01",
    "sel02",
    "sel03",
    "sel04",
    "sel05",
    "sel06",
    "01b",
    "enc01",
    "enc02",
    "enc03",
    "estop",
    "06b",
)
BUTTON_HAS_LONG = (
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    False,
    True,
)


# create hal pins
timer = {}
last = {}
if not args.test:
    import hal

    h = hal.component("mpg")
    for axis in AXIS:
        h.newpin(f"axis.{axis}.pos", hal.HAL_FLOAT, hal.HAL_IN)
        h.newpin(f"axis.{axis}.jog-counts", hal.HAL_S32, hal.HAL_OUT)
        h.newpin(f"axis.{axis}.homed", hal.HAL_BIT, hal.HAL_IN)
    for name in OVERWRITES:
        h.newpin(f"override.{name}.value", hal.HAL_FLOAT, hal.HAL_IN)
        h.newpin(f"override.{name}.counts", hal.HAL_S32, hal.HAL_OUT)
    for num, name in enumerate(BUTTON_NAMES):
        timer[f"button.{name}"] = 0
        last[f"button.{name}"] = False
        h.newpin(f"button.{name}", hal.HAL_BIT, hal.HAL_OUT)
        h.newpin(f"button.{name}-not", hal.HAL_BIT, hal.HAL_OUT)
        h.newpin(f"button.{name}-toggle", hal.HAL_BIT, hal.HAL_OUT)
        h.newpin(f"button.{name}-toggle-not", hal.HAL_BIT, hal.HAL_OUT)
        h.newpin(f"button.{name}-toggle-on", hal.HAL_BIT, hal.HAL_OUT)
        h.newpin(f"button.{name}-toggle-off", hal.HAL_BIT, hal.HAL_OUT)
        if BUTTON_HAS_LONG[num]:
            h.newpin(f"button.{name}-long", hal.HAL_BIT, hal.HAL_OUT)
            h.newpin(f"button.{name}-long-not", hal.HAL_BIT, hal.HAL_OUT)
            h.newpin(f"button.{name}-long-toggle", hal.HAL_BIT, hal.HAL_OUT)
            h.newpin(f"button.{name}-long-toggle-not", hal.HAL_BIT, hal.HAL_OUT)
            h.newpin(f"button.{name}-long-toggle-on", hal.HAL_BIT, hal.HAL_OUT)
            h.newpin(f"button.{name}-long-toggle-off", hal.HAL_BIT, hal.HAL_OUT)

    if args.leds:
        for name in LED_NAMES:
            h.newpin(f"led.{name}", hal.HAL_BIT, hal.HAL_IN)
        h.newpin("axis.selected", hal.HAL_U32, hal.HAL_OUT)
    else:
        for name in LED_NAMES:
            h.newpin(f"led.{name}", hal.HAL_BIT, hal.HAL_OUT)
        h.newpin("axis.selected", hal.HAL_U32, hal.HAL_IN)
    if args.scaler:
        h.newpin("jog-scale", hal.HAL_FLOAT, hal.HAL_OUT)
    else:
        h.newpin("jog-scale", hal.HAL_FLOAT, hal.HAL_IN)
    h.newpin("machine.is-on", hal.HAL_BIT, hal.HAL_IN)
    h.newpin("program.is-running", hal.HAL_BIT, hal.HAL_IN)

    h.ready()
else:
    h = {}
    for axis in AXIS:
        h[f"axis.{axis}.pos"] = 0.0
        h[f"axis.{axis}.jog-counts"] = 0
        h[f"axis.{axis}.homed"] = True
    for name in OVERWRITES:
        h[f"override.{name}.value"] = 0.5
        h[f"override.{name}.counts"] = 0
    for num, name in enumerate(BUTTON_NAMES):
        timer[f"button.{name}"] = 0
        last[f"button.{name}"] = False
        h[f"button.{name}"] = False
        h[f"button.{name}-not"] = True
        h[f"button.{name}-toggle"] = False
        h[f"button.{name}-toggle-not"] = True
        h[f"button.{name}-toggle-on"] = False
        h[f"button.{name}-toggle-off"] = False
        if BUTTON_HAS_LONG[num]:
            h[f"button.{name}-long"] = False
            h[f"button.{name}-long-not"] = True
            h[f"button.{name}-long-toggle"] = False
            h[f"button.{name}-long-toggle-not"] = True
            h[f"button.{name}-long-toggle-on"] = False
            h[f"button.{name}-long-toggle-off"] = False
    for name in LED_NAMES:
        h[f"led.{name}"] = False
    if args.scaler:
        h["jog-scale"] = 0.01
    h["machine.is-on"] = True
    h["program.is-running"] = False


# init serial
ser = serial.Serial(args.device, args.baud, timeout=0.01)
while ser.inWaiting() > 0:
    ser.read(1)

# select x axis by default
if not args.leds:
    h["axis.selected"] = 1

# scaler default
if args.scaler:
    h["jog-scale"] = 0.01


def button_press(base_name):
    h[f"{base_name}"] = True
    h[f"{base_name}-toggle"] = not h[f"{base_name}-toggle"]
    if h[f"{base_name}-toggle"]:
        h[f"{base_name}-toggle-on"] = True
    else:
        h[f"{base_name}-toggle-off"] = True
    # select active axis
    if not args.leds:
        if name.startswith("sel0"):
            anum = int(name[-1])
            if h["axis.selected"] != anum:
                h["axis.selected"] = anum


# main loop
while True:
    try:
        # set led bits
        leds = 0
        for ln, name in enumerate(LED_NAMES):
            if h[f"led.{name}"]:
                leds |= 1 << ln

        if h["machine.is-on"]:
            leds |= 1 << 6
        if h["program.is-running"]:
            leds |= 1 << 7
        for num, axis in enumerate(AXIS):
            if h[f"axis.{axis}.homed"]:
                leds |= 1 << (8+num)



        # pack and send tx data
        data = b""
        for axis in AXIS:
            data += pack("<f", h[f"axis.{axis}.pos"])
        for name in OVERWRITES:
            data += pack("<h", int(h[f"override.{name}.value"] * 100.0))
        data += pack("<H", int(leds))
        data += pack("<f", h[f"jog-scale"])
        data += pack("<f", 0.0)
        data += pack("<f", 0.0)
        ser.write(bytes(data))

        # receive and unpack rx data
        msgFromServer = ser.read(RX_SIZE)
        if msgFromServer and len(msgFromServer) == RX_SIZE:
            # convert rx data
            bpos = 0
            jog_diff = unpack("<h", bytes(msgFromServer[bpos : bpos + 2]))[0]
            bpos += 2
            for name in OVERWRITES:
                h[f"override.{name}.counts"] = unpack("<h", bytes(msgFromServer[bpos : bpos + 2]))[0]
                bpos += 2
            buttons = unpack("<I", bytes(msgFromServer[bpos : bpos + 4]))[0]
            bpos += 4

            # update selected axis (jog diff)
            if not args.leds and h["axis.selected"] > 0:
                h[f"axis.{AXIS[h['axis.selected'] - 1]}.jog-counts"] += int(jog_diff)

            # set buttons halpins
            for num, name in enumerate(BUTTON_NAMES):
                h[f"button.{name}-toggle-on"] = False
                h[f"button.{name}-toggle-off"] = False
                if BUTTON_HAS_LONG[num]:
                    h[f"button.{name}-long-toggle-on"] = False
                    h[f"button.{name}-long-toggle-off"] = False
                    h[f"button.{name}"] = False

                if buttons & (1 << num) != 0:
                    if not last[f"button.{name}"]:
                        if BUTTON_HAS_LONG[num]:
                            timer[f"button.{name}"] = LONG_PRESS
                        else:
                            button_press(f"button.{name}")
                    elif BUTTON_HAS_LONG[num]:
                        if timer[f"button.{name}"] > 1:
                            timer[f"button.{name}"] -= 1
                        elif timer[f"button.{name}"] == 1:
                            timer[f"button.{name}"] = 0
                            button_press(f"button.{name}-long")
                    last[f"button.{name}"] = True
                else:
                    if timer[f"button.{name}"] > 1:
                        timer[f"button.{name}"] = 0
                        button_press(f"button.{name}")

                    if not BUTTON_HAS_LONG[num]:
                        h[f"button.{name}"] = False
                    else:
                        h[f"button.{name}-long"] = False
                    last[f"button.{name}"] = False

                h[f"button.{name}-not"] = not h[f"button.{name}"]
                h[f"button.{name}-toggle-not"] = not h[f"button.{name}-toggle"]
                if BUTTON_HAS_LONG[num]:
                    h[f"button.{name}-long-not"] = not h[f"button.{name}-long"]
                    h[f"button.{name}-long-toggle-not"] = not h[f"button.{name}-long-toggle"]


            # select resolution
            if args.scaler:
                if h["button.06"] == True:
                    h["jog-scale"] = 0.01
                elif h["button.06-long"] == True:
                    h["jog-scale"] = 0.001
                elif h["button.06b"] == True:
                    h["jog-scale"] = 0.1
                elif h["button.06b-long"] == True:
                    h["jog-scale"] = 1.0

            # set led for active axis
            if not args.leds:
                for ln, name in enumerate(LED_NAMES):
                    if (ln + 1) == h["axis.selected"]:
                        h[f"led.{name}"] = True
                    else:
                        h[f"led.{name}"] = False

            # print halpins in testmode
            if args.test:
                for key, value in h.items():
                    print(key, value)
                print("-------------")
                # loop back for testing
                for axis in AXIS:
                    h[f"axis.{axis}.pos"] = h[f"axis.{axis}.jog-counts"] / 10.0
                for name in OVERWRITES:
                    h[f"override.{name}.value"] = h[f"override.{name}.counts"] / 100.0

        # serial sync
        while ser.inWaiting() > 0:
            ser.read(1)
    except IOError as err:
        print(f"MPG: IOERROR: {err}")
        try:
            ser.close()
            if not os.path.isfile(args.device):
                while True:
                    if os.path.exists(args.device):
                        print("MPG: reconnect to device..")
                        ser = serial.Serial(args.device, args.baud, timeout=0.01)
                        while ser.inWaiting() > 0:
                            ser.read(1)
                        break
                    else:
                        print("MPG: wait for device..")
                        time.sleep(1)
        except Exception as err2:
            print(f"MPG: ERROR: {err2}")
    except Exception as err:
        print(f"MPG: ERROR: {err}")
        time.sleep(0.5)

    time.sleep(0.02)
