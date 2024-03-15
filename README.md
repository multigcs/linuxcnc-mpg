# MPG for LinuxCNC

work in progress !!

[![DIY-MPG for LinuxCNC - hal tests](https://img.youtube.com/vi/hYcYCV4b4o4/0.jpg)](https://www.youtube.com/watch?v=hYcYCV4b4o4 "DIY-MPG for LinuxCNC - hal tests")


## TODO
- [x] espnow support (incl. dongle/bridge)
- [x] adding toggle support to the buttons (incl oneshot signals)
- [x] controling LED's and axis switching from python
- [x] transmitting only the diff of the encoder's
- [ ] interception of connection problems
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


## Hal-Configuration (example)
this is for LinuxCNC >= 2.9
``` 
loadusr mpg -d /dev/ttyUSB0

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
