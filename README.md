# Trellis M4 Express Experiments

An assortment of random experiments using the Adafruit [NeoTrellis M4](https://www.adafruit.com/product/4020).


## commtest

Initial experiments into using the serial port interface for bidirectional 
commnunication between the board and the host system.  Features include capturing
button pushes and accelerometer data, and controlling the neopixel matrix.

This will eventually be implemented as modules in CircuitPython and Node.js for
use in other projects (e.g. lifxcontroller)

## lifxcontroller

One of my primary use cases: implement a control system for all the Wifi-enabled
lights and outlets in my home.

Status: working on designing the UI and UX.  Requires the completion of commtest
libraries for full function.

## Rainbow

Discovering the most efficient way of drawing on the neopixel matrix while playing
with the accelerometer.  Animated rainbow gradient moves across the board in the
direction the board is leaning, as if a rainbow waterfall is pouring off the surface.

Status: rainbow animation is implemented and will speed up or slow down based on
tilt.  TODO: change the direction of the flow based on tilt.



# Resources

https://forums.adafruit.com/viewtopic.php?f=60&t=146849

https://learn.adafruit.com/circuitpython-essentials/circuitpython-neopixel

https://circuitpython.readthedocs.io/en/latest/shared-bindings/_pixelbuf/__init__.html

