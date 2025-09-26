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
parser.add_argument("--local", "-c", help="use local controls", type=bool, default=True)
parser.add_argument(
    "--test", "-t", help="test mode / no hal needed", default=False, action="store_true"
)
parser.add_argument(
    "--scaler", "-s", help="scale selctor", default=False, action="store_true"
)
parser.add_argument(
    "--leds",
    "-l",
    help="disable axis selection / led control by hal",
    default=False,
    action="store_true",
)
args = parser.parse_args()

# setup
RX_SIZE = 12 + 8
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
    h.newpin("display-mode", hal.HAL_BIT, hal.HAL_IN)
    h.newpin("mode.is-auto", hal.HAL_BIT, hal.HAL_IN)
    h.newpin("mode.is-manual", hal.HAL_BIT, hal.HAL_IN)
    h.newpin("mode.is-mdi", hal.HAL_BIT, hal.HAL_IN)
    h.newpin("coolant-mist", hal.HAL_BIT, hal.HAL_IN)
    h.newpin("coolant-flood", hal.HAL_BIT, hal.HAL_IN)
    h.newpin("tool-number", hal.HAL_S32, hal.HAL_IN)
    h.newpin("spindle.speed", hal.HAL_FLOAT, hal.HAL_IN)
    h.newpin("connected", hal.HAL_BIT, hal.HAL_OUT)
    h.newpin("csum", hal.HAL_BIT, hal.HAL_OUT)
    h.newpin("header", hal.HAL_BIT, hal.HAL_OUT)

    h.newpin("dongle.analog.jog", hal.HAL_BIT, hal.HAL_IN)
    h.newpin("dongle.analog.01", hal.HAL_FLOAT, hal.HAL_OUT)
    h.newpin("dongle.analog.02", hal.HAL_FLOAT, hal.HAL_OUT)
    h.newpin("dongle.analog.03", hal.HAL_FLOAT, hal.HAL_OUT)
    h.newpin("dongle.button.01", hal.HAL_BIT, hal.HAL_OUT)

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
    h["jog-scale"] = 0.01
    h["machine.is-on"] = True
    h["program.is-running"] = False
    h["display-mode"] = False
    h["mode.is-auto"] = False
    h["mode.is-manual"] = False
    h["mode.is-mdi"] = False
    h["coolant-mist"] = False
    h["coolant-flood"] = False
    h["tool-number"] = 0
    h["spindle.speed"] = 0.0
    h["connected"] = False
    h["csum"] = False
    h["header"] = False
    h["dongle.analog.jog"] = True
    h["dongle.analog.01"] = 0.0
    h["dongle.analog.02"] = 0.0
    h["dongle.analog.03"] = 0.0
    h["dongle.button.01"] = 0


# init serial
ser = serial.Serial(args.device, args.baud, timeout=0.03)
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


analog_center = [0, 0, 0]
# main loop
while True:
    try:
        # set led bits
        leds = 0
        for ln, name in enumerate(LED_NAMES):
            if h[f"led.{name}"]:
                leds |= 1 << ln
        for num, axis in enumerate(AXIS):
            if h[f"axis.{axis}.homed"]:
                leds |= 1 << (8 + num)

        stats = 0
        if h["display-mode"]:
            stats |= 1 << 0
        if h["machine.is-on"]:
            stats |= 1 << 1
        if h["program.is-running"]:
            stats |= 1 << 2
        if h["mode.is-auto"]:
            stats |= 1 << 3
        if h["mode.is-manual"]:
            stats |= 1 << 4
        if h["mode.is-mdi"]:
            stats |= 1 << 5
        if h["coolant-mist"]:
            stats |= 1 << 6
        if h["coolant-flood"]:
            stats |= 1 << 7

        # serial sync
        #        while ser.inWaiting() > 0:
        #            ser.read(1)

        # pack and send tx data
        data = b""
        data += bytes([99, 18, 27, 36])
        for axis in AXIS:
            data += pack("<f", h[f"axis.{axis}.pos"])
        for name in OVERWRITES:
            data += pack("<h", int(h[f"override.{name}.value"] * 100.0))
        data += pack("<H", int(leds))
        data += pack("<f", h["jog-scale"])
        data += pack("<f", h["spindle.speed"])
        data += pack("<H", int(stats))
        data += pack("<B", int(h["tool-number"]))
        data += pack("<B", int(0))
        data += bytes([sum(data[4:]) & 255])

        ser.write(bytes(data))

        # receive and unpack rx data
        """
        timeout = 10
        while timeout > 0:
            rxc = ser.read(1)
            if rxc[0] == 123:
                break
            print("#", int(rxc[0]))
            time.sleep(0.01)
            timeout -= 1
        """

        msgFromServer = ser.read(RX_SIZE + 5)

        if args.test:
            print("RX", [int(byte) for byte in msgFromServer])

        if msgFromServer and len(msgFromServer) == RX_SIZE + 5:
            if (
                int(msgFromServer[0]) == 123
                and int(msgFromServer[1]) == 234
                and int(msgFromServer[2]) == 222
                and int(msgFromServer[3]) == 111
            ):
                if args.test:
                    print("HEADER OK")
                h["header"] = True
            else:
                if args.test:
                    print("HEADER ERROR")
                h["header"] = False
                continue

            if msgFromServer[-1] == sum(msgFromServer[0:-1]) & 255:
                if args.test:
                    print("CSUM OK")
                h["csum"] = True
            else:
                if args.test:
                    print("CSUM ERROR")
                h["csum"] = False
                continue

            h["connected"] = True

            # convert rx data
            bpos = 4
            jog_diff = unpack("<h", bytes(msgFromServer[bpos : bpos + 2]))[0]
            bpos += 2
            for name in OVERWRITES:
                h[f"override.{name}.counts"] = unpack(
                    "<h", bytes(msgFromServer[bpos : bpos + 2])
                )[0]
                bpos += 2
            buttons = unpack("<I", bytes(msgFromServer[bpos : bpos + 4]))[0]
            bpos += 4

            adc0 = unpack("<h", bytes(msgFromServer[bpos : bpos + 2]))[0]
            bpos += 2
            adc1 = unpack("<h", bytes(msgFromServer[bpos : bpos + 2]))[0]
            bpos += 2
            adc2 = unpack("<h", bytes(msgFromServer[bpos : bpos + 2]))[0]
            bpos += 2

            if analog_center[0] == 0:
                analog_center[0] = adc0
                analog_center[1] = adc1
                analog_center[2] = adc2

            adc0 = min(max(int((adc0 - analog_center[0]) / 16), -100), 100)
            adc1 = min(max(int((adc1 - analog_center[1]) / 16), -100), 100)
            adc2 = min(max(int((adc2 - analog_center[2]) / 16), -100), 100)
            h["dongle.analog.01"] = -adc0
            h["dongle.analog.02"] = -adc1
            h["dongle.analog.03"] = -adc2
            if h["dongle.analog.jog"]:
                h[f"axis.{AXIS[0]}.jog-counts"] += int(h["dongle.analog.01"] / 5)
                h[f"axis.{AXIS[1]}.jog-counts"] += int(h["dongle.analog.02"] / 5)
                h[f"axis.{AXIS[2]}.jog-counts"] += int(h["dongle.analog.03"] / 5)

            abuttons = unpack("<h", bytes(msgFromServer[bpos : bpos + 2]))[0]
            bpos += 2
            h["dongle.button.01"] = abuttons

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
                    h[f"button.{name}-long-toggle-not"] = not h[
                        f"button.{name}-long-toggle"
                    ]

            # select resolution
            if args.scaler:
                if h["button.06"] is True:
                    h["jog-scale"] = 0.01
                elif h["button.06-long"] is True:
                    h["jog-scale"] = 0.001
                elif h["button.06b"] is True:
                    h["jog-scale"] = 0.1
                elif h["button.06b-long"] is True:
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

                # loop back for testing
                for axis in AXIS:
                    h[f"axis.{axis}.pos"] = h[f"axis.{axis}.jog-counts"] / 10.0
                for name in OVERWRITES:
                    h[f"override.{name}.value"] = h[f"override.{name}.counts"] / 100.0
        else:
            h["connected"] = False

            if args.test:
                for key, value in h.items():
                    print(key, value)

                # loop back for testing
                for axis in AXIS:
                    h[f"axis.{axis}.pos"] = h[f"axis.{axis}.jog-counts"] / 10.0
                for name in OVERWRITES:
                    h[f"override.{name}.value"] = h[f"override.{name}.counts"] / 100.0
            time.sleep(1)

    except IOError as err:
        print(f"MPG: IOERROR: {err}")
        try:
            ser.close()
            if not os.path.isfile(args.device):
                while True:
                    if os.path.exists(args.device):
                        print("MPG: reconnect to device..")
                        ser = serial.Serial(args.device, args.baud, timeout=0.03)
                        # while ser.inWaiting() > 0:
                        #    ser.read(1)
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
