# Optical Hardware Control

## Purpose
This tool is designed to control simple actuators such as shutters or rotators for optical experiments using a microcontroller with Python.


## Server (microcontroller)


### Installation 

Copy the content of the *circuit_python* folder to the memory of the microcontroller.
The code provided has been tested with Adafruit boards with a M4 chip.
If you use a different board, please replace the content of the lib folder by the corresponding appropriate modules.


### Usage

In the main.py

#### Import the necessary modules

```Python
from rotator import Rotator
from shutter import Shutter
from com import Com
```

#### Connect a shutter

Use the design and instructions available here to build a cheal optical shutter: [github.com/wavefrontshaping/Servo-Motor-Shutter](https://github.com/wavefrontshaping/Servo-Motor-Shutter).

It requires only one pin to control the servo motor. 
Change the pin value accordingly.

```Python
myservo = Shutter(board.D7)
```

We now add the shutter to the `Com` object. 
It will listen and wait for commands associated with the device once the `wait_for_cmd()` is called.

```Python
mycom.register_device('shutter', myservo.cmd)
```

#### Connect a rotator

*To come...*

#### Listen and wait for commands.

```Python
mycom.register_device('shutter', myservo.cmd)
```

## Client (computer)

### Installation 

Copy the file `python_control_module\hardware_cmd.py` to your current working directory.

### Shutter

```Python
from hardware_cmd import Shutter
import time

shutter = Shutter(port = '/dev/ttyACM0')
# on window it would look like (port = 'COM4')
# change port number accordingly
shutter.go_to(0)
time.sleep(0.5)
shutter.set_pos('open',45)
shutter.go_to('open')
time.sleep(0.5)
shutter.go_to(22.5)
shutter.close()
```

### Rotator

```Python
from hardware_cmd import Rotator
rot = Rotator(port = '/dev/ttyACM0')
# on window it would look like (port = 'COM4')
# change port number accordingly
rot.home(fast = True)
rot.set_mode('forward')
rot.go_to(20)
print(rot.get_angle())
rot.set_speed(100)
rot.go_to(10)
print(rot.get_angle())
rot.close()
```
