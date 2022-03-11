import math
from micropython import const

# Constants that specify the direction and style of steps.
FORWARD = const(1)
"""Step forward"""
BACKWARD = const(2)
""""Step backward"""

class StepperMotor:
    """A bipolar stepper motor or four coil unipolar motor.
    :param ~pulseio.PWMOut ain1: `pulseio.PWMOut`-compatible output connected to the driver for
      the first coil (unipolar) or first input to first coil (bipolar).
    :param ~pulseio.PWMOut ain2: `pulseio.PWMOut`-compatible output connected to the driver for
      the third coil (unipolar) or second input to first coil (bipolar).
    :param ~pulseio.PWMOut bin1: `pulseio.PWMOut`-compatible output connected to the driver for
      the second coil (unipolar) or second input to second coil (bipolar).
    :param ~pulseio.PWMOut bin2: `pulseio.PWMOut`-compatible output connected to the driver for
      the fourth coil (unipolar) or second input to second coil (bipolar).
    :param int microsteps: Number of microsteps between full steps. Must be at least 2 and even.
    """
    def __init__(self, ain1, ain2, bin1, bin2, *, microsteps=16):
        self._coil = (ain2, bin1, ain1, bin2)

	# set a safe pwm freq for each output
        ##for i in range(4):
        #    if self._coil[i].frequency < 1500:
        #        self._coil[i].frequency = 2000

        self._current_step = 0
        if microsteps < 2:
            raise ValueError("Microsteps must be at least 2")
        if microsteps % 2 == 1:
            raise ValueError("Microsteps must be even")
        self._microsteps = microsteps
        self._curve = [int(round(0xffff * math.sin(math.pi / (2 * microsteps) * i)))
                       for i in range(microsteps + 1)]
        #self._update_coils()

    def step(self,*, direction=FORWARD):
        sequence = [
            [0x0000,0x0000,0x0000,0x0000,0x0000,0xffff,0xffff,0xffff],
            [0x0000,0x0000,0x0000,0xffff,0xffff,0xffff,0x0000,0x0000],
            [0x0000,0xffff,0xffff,0xffff,0x0000,0x0000,0x0000,0x0000],
            [0xffff,0xffff,0x0000,0x0000,0x0000,0x0000,0x0000,0xffff]
        ]
        if direction == FORWARD:
            self._current_step += 1
        else:
            self._current_step -= 1

        for i in range(4):
            self._coil[i].duty_cycle = sequence[i][self._current_step % 8]
        
        return self._current_step
 

    def release(self):
        """Releases all the coils so the motor can free spin, also won't use any power"""
        # De-energize coils:
        for i in range(4):
            self._coil[i].duty_cycle = 0

  