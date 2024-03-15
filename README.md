# MPG for LinuxCNC

work in progress !!

https://www.youtube.com/watch?v=mJ1qc-PS2gQ

[![DIY-MPG for LinuxCNC - wireless](https://img.youtube.com/vi/mJ1qc-PS2gQ/0.jpg)](https://www.youtube.com/watch?v=mJ1qc-PS2gQ "DIY-MPG for LinuxCNC - wireless")
[![DIY-MPG for LinuxCNC - hal tests](https://img.youtube.com/vi/hYcYCV4b4o4/0.jpg)](https://www.youtube.com/watch?v=hYcYCV4b4o4 "DIY-MPG for LinuxCNC - hal tests")


## TODO
- [x] espnow support (incl. dongle/bridge)
- [x] adding toggle support to the buttons (incl oneshot signals)
- [x] controling LED's and axis switching from python
- [x] transmitting only the diff of the encoder's
- [x] interception of connection problems
- [ ] adding LIPO with wireless and USB charger
- [ ] adding ADC to check LIPO voltage
- [ ] better GUI / maybe touch support (if i found a free usable pin)
- [ ] more values/halpins to display
- [ ] full hal examples


## BOM

| number | name | link |
| --- | --- | --- |
| 1 | S2 Mini V1.0.0 ESP32-S2 Modul | https://www.amazon.de/dp/B0CJHWD986 |
| 1 | 2.4Zoll TFT-Display (ILI9341) | https://www.amazon.de/dp/B0CC8V17GS |
| 1 | Emergency stop switch | https://www.amazon.de/dp/B08ZS8HZYV |
| 1 | rotary encoder | https://www.amazon.de/dp/B07MFVK8QT |
| 3 | rotary encoder with push button | https://www.amazon.de/dp/B096NYWY2M |
| 6 | 3mm LED | https://www.amazon.de/dp/B07Q1813PN |
| 14 | 12x12 momentary switch | https://www.amazon.de/dp/B07JBXS6RC |
| 1 | Resistor ~680Ohm | |



## Compile and Load Firmware
you need a working platformio installation (https://platformio.org/install)
```
cd pendant
pio run --target upload
```

if you need a wireless connection (needs 2. ESP32S2):
```
cd dongle
pio run --target upload
```


## Install Hal-Component
```
sudo cp linuxcnc/mpg.py /usr/local/bin/mpg
sudo chmod 755 /usr/local/bin/mpg
``` 

## Hal-Pins

| name | dir | type |
| --- | --- | --- |
| mpg.axis.a.homed | IN | bit |
| mpg.axis.a.jog-counts | OUT | s32 |
| mpg.axis.a.pos | IN | float |
| mpg.axis.b.homed | IN | bit |
| mpg.axis.b.jog-counts | OUT | s32 |
| mpg.axis.b.pos | IN | float |
| mpg.axis.c.homed | IN | bit |
| mpg.axis.c.jog-counts | OUT | s32 |
| mpg.axis.c.pos | IN | float |
| mpg.axis.selected | IN | u32 |
| mpg.axis.x.homed | IN | bit |
| mpg.axis.x.jog-counts | OUT | s32 |
| mpg.axis.x.pos | IN | float |
| mpg.axis.y.homed | IN | bit |
| mpg.axis.y.jog-counts | OUT | s32 |
| mpg.axis.y.pos | IN | float |
| mpg.axis.z.homed | IN | bit |
| mpg.axis.z.jog-counts | OUT | s32 |
| mpg.axis.z.pos | IN | float |
| mpg.button.01 | OUT | bit |
| mpg.button.01-long | OUT | bit |
| mpg.button.01-long-not | OUT | bit |
| mpg.button.01-long-toggle | OUT | bit |
| mpg.button.01-long-toggle-not | OUT | bit |
| mpg.button.01-long-toggle-off | OUT | bit |
| mpg.button.01-long-toggle-on | OUT | bit |
| mpg.button.01-not | OUT | bit |
| mpg.button.01-toggle | OUT | bit |
| mpg.button.01-toggle-not | OUT | bit |
| mpg.button.01-toggle-off | OUT | bit |
| mpg.button.01-toggle-on | OUT | bit |
| mpg.button.01b | OUT | bit |
| mpg.button.01b-long | OUT | bit |
| mpg.button.01b-long-not | OUT | bit |
| mpg.button.01b-long-toggle | OUT | bit |
| mpg.button.01b-long-toggle-not | OUT | bit |
| mpg.button.01b-long-toggle-off | OUT | bit |
| mpg.button.01b-long-toggle-on | OUT | bit |
| mpg.button.01b-not | OUT | bit |
| mpg.button.01b-toggle | OUT | bit |
| mpg.button.01b-toggle-not | OUT | bit |
| mpg.button.01b-toggle-off | OUT | bit |
| mpg.button.01b-toggle-on | OUT | bit |
| mpg.button.02 | OUT | bit |
| mpg.button.02-long | OUT | bit |
| mpg.button.02-long-not | OUT | bit |
| mpg.button.02-long-toggle | OUT | bit |
| mpg.button.02-long-toggle-not | OUT | bit |
| mpg.button.02-long-toggle-off | OUT | bit |
| mpg.button.02-long-toggle-on | OUT | bit |
| mpg.button.02-not | OUT | bit |
| mpg.button.02-toggle | OUT | bit |
| mpg.button.02-toggle-not | OUT | bit |
| mpg.button.02-toggle-off | OUT | bit |
| mpg.button.02-toggle-on | OUT | bit |
| mpg.button.03 | OUT | bit |
| mpg.button.03-long | OUT | bit |
| mpg.button.03-long-not | OUT | bit |
| mpg.button.03-long-toggle | OUT | bit |
| mpg.button.03-long-toggle-not | OUT | bit |
| mpg.button.03-long-toggle-off | OUT | bit |
| mpg.button.03-long-toggle-on | OUT | bit |
| mpg.button.03-not | OUT | bit |
| mpg.button.03-toggle | OUT | bit |
| mpg.button.03-toggle-not | OUT | bit |
| mpg.button.03-toggle-off | OUT | bit |
| mpg.button.03-toggle-on | OUT | bit |
| mpg.button.04 | OUT | bit |
| mpg.button.04-long | OUT | bit |
| mpg.button.04-long-not | OUT | bit |
| mpg.button.04-long-toggle | OUT | bit |
| mpg.button.04-long-toggle-not | OUT | bit |
| mpg.button.04-long-toggle-off | OUT | bit |
| mpg.button.04-long-toggle-on | OUT | bit |
| mpg.button.04-not | OUT | bit |
| mpg.button.04-toggle | OUT | bit |
| mpg.button.04-toggle-not | OUT | bit |
| mpg.button.04-toggle-off | OUT | bit |
| mpg.button.04-toggle-on | OUT | bit |
| mpg.button.05 | OUT | bit |
| mpg.button.05-long | OUT | bit |
| mpg.button.05-long-not | OUT | bit |
| mpg.button.05-long-toggle | OUT | bit |
| mpg.button.05-long-toggle-not | OUT | bit |
| mpg.button.05-long-toggle-off | OUT | bit |
| mpg.button.05-long-toggle-on | OUT | bit |
| mpg.button.05-not | OUT | bit |
| mpg.button.05-toggle | OUT | bit |
| mpg.button.05-toggle-not | OUT | bit |
| mpg.button.05-toggle-off | OUT | bit |
| mpg.button.05-toggle-on | OUT | bit |
| mpg.button.06 | OUT | bit |
| mpg.button.06-long | OUT | bit |
| mpg.button.06-long-not | OUT | bit |
| mpg.button.06-long-toggle | OUT | bit |
| mpg.button.06-long-toggle-not | OUT | bit |
| mpg.button.06-long-toggle-off | OUT | bit |
| mpg.button.06-long-toggle-on | OUT | bit |
| mpg.button.06-not | OUT | bit |
| mpg.button.06-toggle | OUT | bit |
| mpg.button.06-toggle-not | OUT | bit |
| mpg.button.06-toggle-off | OUT | bit |
| mpg.button.06-toggle-on | OUT | bit |
| mpg.button.06b | OUT | bit |
| mpg.button.06b-long | OUT | bit |
| mpg.button.06b-long-not | OUT | bit |
| mpg.button.06b-long-toggle | OUT | bit |
| mpg.button.06b-long-toggle-not | OUT | bit |
| mpg.button.06b-long-toggle-off | OUT | bit |
| mpg.button.06b-long-toggle-on | OUT | bit |
| mpg.button.06b-not | OUT | bit |
| mpg.button.06b-toggle | OUT | bit |
| mpg.button.06b-toggle-not | OUT | bit |
| mpg.button.06b-toggle-off | OUT | bit |
| mpg.button.06b-toggle-on | OUT | bit |
| mpg.button.enc01 | OUT | bit |
| mpg.button.enc01-long | OUT | bit |
| mpg.button.enc01-long-not | OUT | bit |
| mpg.button.enc01-long-toggle | OUT | bit |
| mpg.button.enc01-long-toggle-not | OUT | bit |
| mpg.button.enc01-long-toggle-off | OUT | bit |
| mpg.button.enc01-long-toggle-on | OUT | bit |
| mpg.button.enc01-not | OUT | bit |
| mpg.button.enc01-toggle | OUT | bit |
| mpg.button.enc01-toggle-not | OUT | bit |
| mpg.button.enc01-toggle-off | OUT | bit |
| mpg.button.enc01-toggle-on | OUT | bit |
| mpg.button.enc02 | OUT | bit |
| mpg.button.enc02-long | OUT | bit |
| mpg.button.enc02-long-not | OUT | bit |
| mpg.button.enc02-long-toggle | OUT | bit |
| mpg.button.enc02-long-toggle-not | OUT | bit |
| mpg.button.enc02-long-toggle-off | OUT | bit |
| mpg.button.enc02-long-toggle-on | OUT | bit |
| mpg.button.enc02-not | OUT | bit |
| mpg.button.enc02-toggle | OUT | bit |
| mpg.button.enc02-toggle-not | OUT | bit |
| mpg.button.enc02-toggle-off | OUT | bit |
| mpg.button.enc02-toggle-on | OUT | bit |
| mpg.button.enc03 | OUT | bit |
| mpg.button.enc03-long | OUT | bit |
| mpg.button.enc03-long-not | OUT | bit |
| mpg.button.enc03-long-toggle | OUT | bit |
| mpg.button.enc03-long-toggle-not | OUT | bit |
| mpg.button.enc03-long-toggle-off | OUT | bit |
| mpg.button.enc03-long-toggle-on | OUT | bit |
| mpg.button.enc03-not | OUT | bit |
| mpg.button.enc03-toggle | OUT | bit |
| mpg.button.enc03-toggle-not | OUT | bit |
| mpg.button.enc03-toggle-off | OUT | bit |
| mpg.button.enc03-toggle-on | OUT | bit |
| mpg.button.estop | OUT | bit |
| mpg.button.estop-not | OUT | bit |
| mpg.button.estop-toggle | OUT | bit |
| mpg.button.estop-toggle-not | OUT | bit |
| mpg.button.estop-toggle-off | OUT | bit |
| mpg.button.estop-toggle-on | OUT | bit |
| mpg.button.sel01 | OUT | bit |
| mpg.button.sel01-long | OUT | bit |
| mpg.button.sel01-long-not | OUT | bit |
| mpg.button.sel01-long-toggle | OUT | bit |
| mpg.button.sel01-long-toggle-not | OUT | bit |
| mpg.button.sel01-long-toggle-off | OUT | bit |
| mpg.button.sel01-long-toggle-on | OUT | bit |
| mpg.button.sel01-not | OUT | bit |
| mpg.button.sel01-toggle | OUT | bit |
| mpg.button.sel01-toggle-not | OUT | bit |
| mpg.button.sel01-toggle-off | OUT | bit |
| mpg.button.sel01-toggle-on | OUT | bit |
| mpg.button.sel02 | OUT | bit |
| mpg.button.sel02-long | OUT | bit |
| mpg.button.sel02-long-not | OUT | bit |
| mpg.button.sel02-long-toggle | OUT | bit |
| mpg.button.sel02-long-toggle-not | OUT | bit |
| mpg.button.sel02-long-toggle-off | OUT | bit |
| mpg.button.sel02-long-toggle-on | OUT | bit |
| mpg.button.sel02-not | OUT | bit |
| mpg.button.sel02-toggle | OUT | bit |
| mpg.button.sel02-toggle-not | OUT | bit |
| mpg.button.sel02-toggle-off | OUT | bit |
| mpg.button.sel02-toggle-on | OUT | bit |
| mpg.button.sel03 | OUT | bit |
| mpg.button.sel03-long | OUT | bit |
| mpg.button.sel03-long-not | OUT | bit |
| mpg.button.sel03-long-toggle | OUT | bit |
| mpg.button.sel03-long-toggle-not | OUT | bit |
| mpg.button.sel03-long-toggle-off | OUT | bit |
| mpg.button.sel03-long-toggle-on | OUT | bit |
| mpg.button.sel03-not | OUT | bit |
| mpg.button.sel03-toggle | OUT | bit |
| mpg.button.sel03-toggle-not | OUT | bit |
| mpg.button.sel03-toggle-off | OUT | bit |
| mpg.button.sel03-toggle-on | OUT | bit |
| mpg.button.sel04 | OUT | bit |
| mpg.button.sel04-long | OUT | bit |
| mpg.button.sel04-long-not | OUT | bit |
| mpg.button.sel04-long-toggle | OUT | bit |
| mpg.button.sel04-long-toggle-not | OUT | bit |
| mpg.button.sel04-long-toggle-off | OUT | bit |
| mpg.button.sel04-long-toggle-on | OUT | bit |
| mpg.button.sel04-not | OUT | bit |
| mpg.button.sel04-toggle | OUT | bit |
| mpg.button.sel04-toggle-not | OUT | bit |
| mpg.button.sel04-toggle-off | OUT | bit |
| mpg.button.sel04-toggle-on | OUT | bit |
| mpg.button.sel05 | OUT | bit |
| mpg.button.sel05-long | OUT | bit |
| mpg.button.sel05-long-not | OUT | bit |
| mpg.button.sel05-long-toggle | OUT | bit |
| mpg.button.sel05-long-toggle-not | OUT | bit |
| mpg.button.sel05-long-toggle-off | OUT | bit |
| mpg.button.sel05-long-toggle-on | OUT | bit |
| mpg.button.sel05-not | OUT | bit |
| mpg.button.sel05-toggle | OUT | bit |
| mpg.button.sel05-toggle-not | OUT | bit |
| mpg.button.sel05-toggle-off | OUT | bit |
| mpg.button.sel05-toggle-on | OUT | bit |
| mpg.button.sel06 | OUT | bit |
| mpg.button.sel06-long | OUT | bit |
| mpg.button.sel06-long-not | OUT | bit |
| mpg.button.sel06-long-toggle | OUT | bit |
| mpg.button.sel06-long-toggle-not | OUT | bit |
| mpg.button.sel06-long-toggle-off | OUT | bit |
| mpg.button.sel06-long-toggle-on | OUT | bit |
| mpg.button.sel06-not | OUT | bit |
| mpg.button.sel06-toggle | OUT | bit |
| mpg.button.sel06-toggle-not | OUT | bit |
| mpg.button.sel06-toggle-off | OUT | bit |
| mpg.button.sel06-toggle-on | OUT | bit |
| mpg.jog-scale | OUT | float |
| mpg.led.01 | OUT | bit |
| mpg.led.02 | OUT | bit |
| mpg.led.03 | OUT | bit |
| mpg.led.04 | OUT | bit |
| mpg.led.05 | OUT | bit |
| mpg.led.06 | OUT | bit |
| mpg.machine.is-on | IN | bit |
| mpg.override.feed.counts | OUT | s32 |
| mpg.override.feed.value | IN | float |
| mpg.override.rapid.counts | OUT | s32 |
| mpg.override.rapid.value | IN | float |
| mpg.override.spindle.counts | OUT | s32 |
| mpg.override.spindle.value | IN | float |
| mpg.program.is-running | IN | bit |


## Hal-Configuration
this is for LinuxCNC >= 2.9

### example1
``` 
loadusr mpg -d /dev/ttyACM0 -s

# MPG
#net iocontrol_0_emc-enable-in <= mpg.button.estop-not
#net iocontrol_0_emc-enable-in => iocontrol.0.emc-enable-in

net spindle_start <= mpg.button.01
net spindle_start => halui.spindle.0.start

net spindle_stop <= mpg.button.01b
net spindle_stop => halui.spindle.0.stop

setp joint.0.jog-vel-mode 1
setp joint.0.jog-scale 0.01
setp joint.0.jog-enable 1
setp axis.x.jog-vel-mode 1
setp axis.x.jog-scale 0.01
setp axis.x.jog-enable 1
net axis_x_jog-counts <= mpg.axis.x.jog-counts
net axis_x_jog-counts => axis.x.jog-counts
net axis_x_jog-counts => joint.0.jog-counts

setp joint.1.jog-vel-mode 1
setp joint.1.jog-scale 0.01
setp joint.1.jog-enable 1
setp axis.y.jog-vel-mode 1
setp axis.y.jog-scale 0.01
setp axis.y.jog-enable 1
net axis_y_jog-counts <= mpg.axis.y.jog-counts
net axis_y_jog-counts => axis.y.jog-counts
net xis_y_jog-counts => joint.1.jog-counts

net display_x halui.axis.x.pos-relative => mpg.axis.x.pos
net display_y halui.axis.y.pos-relative => mpg.axis.y.pos
net display_z halui.axis.z.pos-relative => mpg.axis.z.pos

setp halui.feed-override.scale 0.01
net feed-override <= mpg.override.feed.counts
net feed-override => halui.feed-override.counts

setp halui.rapid-override.scale 0.01
net rapid-override <= mpg.override.rapid.counts
net rapid-override => halui.rapid-override.counts

setp halui.spindle.0.override.scale 0.01
net spindle-override <= mpg.override.spindle.counts
net spindle-override => halui.spindle.0.override.counts

net override-feed-value <= halui.feed-override.value
net override-feed-value => mpg.override.feed.value

net override-rapid-value <= halui.rapid-override.value
net override-rapid-value => mpg.override.rapid.value

net override-spindle-value <= halui.spindle.0.override.value
net override-spindle-value => mpg.override.spindle.value

``` 


### example2

```
loadusr mpg -d /dev/ttyACM0 -s

#net rios.iocontrol_0_emc-enable-in <= mpg.button.estop-not
#net rios.iocontrol_0_emc-enable-in => iocontrol.0.emc-enable-in


net rios.x_select <= mpg.button.sel01
net rios.x_select => halui.axis.x.select
net rios.y_select <= mpg.button.sel02
net rios.y_select => halui.axis.y.select
net rios.z_select <= mpg.button.sel03
net rios.z_select => halui.axis.z.select


net rios.zero_x <= mpg.button.sel01-long
net rios.zero_x => halui.mdi-command-00
net rios.zero_y <= mpg.button.sel02-long
net rios.zero_y => halui.mdi-command-01
net rios.zero_z <= mpg.button.sel03-long
net rios.zero_z => halui.mdi-command-02

net rios.halui_machine_is-on => mpg.machine.is-on
net rios.halui_program_is-running => mpg.program.is-running

net rios.program_run <= mpg.button.01
net rios.program_run => halui.program.run
net rios.program_stop <= mpg.button.01-long
net rios.program_stop => halui.program.stop
net rios.program_pause <= mpg.button.01b
net rios.program_pause => halui.program.pause
net rios.program_resume <= mpg.button.01b-long
net rios.program_resume => halui.program.resume

net rios.x_homed <= joint.0.homed
net rios.x_homed => mpg.axis.x.homed
net rios.y_homed <= joint.1.homed
net rios.y_homed => mpg.axis.y.homed
net rios.z_homed <= joint.2.homed
net rios.z_homed => mpg.axis.z.homed

net rios.spindle_start <= mpg.button.02-long
net rios.spindle_start => halui.spindle.0.start

net rios.spindle_stop <= mpg.button.02
net rios.spindle_stop => halui.spindle.0.stop

net rios.jog-scale <= mpg.jog-scale
net rios.jog-scale => joint.0.jog-scale
net rios.jog-scale => axis.x.jog-scale
net rios.jog-scale => joint.1.jog-scale
net rios.jog-scale => axis.y.jog-scale

setp joint.0.jog-vel-mode 1
setp joint.0.jog-enable 1
setp axis.x.jog-vel-mode 1
setp axis.x.jog-enable 1
net rios.axis_x_jog-counts <= mpg.axis.x.jog-counts
net rios.axis_x_jog-counts => axis.x.jog-counts
net rios.axis_x_jog-counts => joint.0.jog-counts

setp joint.1.jog-vel-mode 1
setp joint.1.jog-enable 1
setp axis.y.jog-vel-mode 1
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
```
