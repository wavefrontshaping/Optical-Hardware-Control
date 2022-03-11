
# screen /dev/ttyACM0 115200
import board
# from adafruit_motor import stepper
from rotator import Rotator
from shutter import Shutter
from com import Com

import supervisor



# switch off status led
supervisor.set_rgb_status_brightness(0)

# Setup servo
myservo = Shutter(board.D7)

# Setup rotator
home_pin = board.D9
stepper_pins = (board.D10, board.D11, board.D12, board.D13)
myrotator = Rotator(stepper_pins=stepper_pins, home_pin=home_pin)

mycom = Com()
mycom.register_device('rotator', myrotator.cmd)
mycom.register_device('shutter', myservo.cmd)
mycom.wait_for_cmd()



# myrotator = Rotator(stepper_pins=stepper_pins, home_pin=home_pin)
# myrotator.set_mode('forward')
# myrotator.go_home(fast=False)
# while True:
#     print(myrotator.get_angle())
#     myrotator.go_to_angle(30)
#     print(myrotator.get_angle())
#     myrotator.go_to_angle(10)
#     print(myrotator.get_angle())