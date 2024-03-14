#!/usr/bin/env python3
"""

loadusr mpg

# MPG
#net rios.iocontrol_0_emc-enable-in <= mpg.button.estop-not
#net rios.iocontrol_0_emc-enable-in => iocontrol.0.emc-enable-in

net rios.spindle_start <= mpg.button.01
net rios.spindle_start => halui.spindle.0.start

net rios.spindle_stop <= mpg.button.01b
net rios.spindle_stop => halui.spindle.0.stop

setp joint.0.jog-vel-mode 1
setp joint.0.jog-scale 0.01
setp joint.0.jog-enable 1
setp axis.x.jog-vel-mode 1
setp axis.x.jog-scale 0.01
setp axis.x.jog-enable 1
net rios.axis_x_jog-counts <= mpg.axis.x.jog-counts
net rios.axis_x_jog-counts => axis.x.jog-counts
net rios.axis_x_jog-counts => joint.0.jog-counts

setp joint.1.jog-vel-mode 1
setp joint.1.jog-scale 0.01
setp joint.1.jog-enable 1
setp axis.y.jog-vel-mode 1
setp axis.y.jog-scale 0.01
setp axis.y.jog-enable 1
net rios.axis_y_jog-counts <= mpg.axis.y.jog-counts
net rios.axis_y_jog-counts => axis.y.jog-counts
net rios.axis_y_jog-counts => joint.1.jog-counts

net display_x halui.axis.x.pos-relative => mpg.axis.x.pos
net display_y halui.axis.y.pos-relative => mpg.axis.y.pos
net display_z halui.axis.z.pos-relative => mpg.axis.z.pos

setp halui.feed-override.scale 0.01
net rios.feed-override <= mpg.override.feed.counts
net rios.feed-override => halui.feed-override.counts

setp halui.rapid-override.scale 0.01
net rios.rapid-override <= mpg.override.rapid.counts
net rios.rapid-override => halui.rapid-override.counts

setp halui.spindle.0.override.scale 0.01
net rios.spindle-override <= mpg.override.spindle.counts
net rios.spindle-override => halui.spindle.0.override.counts

net rios.override-feed-value <= halui.feed-override.value
net rios.override-feed-value => mpg.override.feed.value

net rios.override-rapid-value <= halui.rapid-override.value
net rios.override-rapid-value => mpg.override.rapid.value

net rios.override-spindle-value <= halui.spindle.0.override.value
net rios.override-spindle-value => mpg.override.spindle.value

"""

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

