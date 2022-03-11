import time
import board
import pulseio, digitalio, busio
import stepper

FREQUENCY = 15000

class Rotator():
    def __init__(self,stepper_pins,home_pin):
        stepper_ios = [pulseio.PWMOut(pin, frequency=FREQUENCY, duty_cycle=0) for pin in stepper_pins]
        order = [3,1,2,0]
        self._sleep_time = 0.0002
        self.button = digitalio.DigitalInOut(home_pin)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.DOWN
        self.stepper = stepper.StepperMotor(*(stepper_ios[i] for i in order))
        self.direction = stepper.FORWARD
        self.home_set = False
        self.speed = 1000
        self.homing_speed_1 = 400
        self.homing_speed_2 = 40
        self.ratio = 4096*52/10#steps per 360 degrees
        self.mode = 'direct'
        self.steps_backward = 400

        
        #self.steps = [ []]


    def go_home(self, fast=False):
        if self.home_set:
            self.go_to_angle(10, mode='direct')
            #if home already set, get closer before homing slowly
        self.direction = stepper.BACKWARD
        # first run to find home
        speed = self.homing_speed_1
        while self.button.value:
            time.sleep(1./speed)
            self._step()
        
        if not fast:
            # move few steps
            for _ in range(300):
                time.sleep(1./speed)
                self.direction = stepper.FORWARD
                self._step()
            # second run to find home, but slower
            speed = self.homing_speed_2
            self.direction = stepper.BACKWARD
            while self.button.value:
                time.sleep(1./speed)
                self._step()
        self.stepper.release()
        self.home_set = True
        self.stepper._current_step = 0
        self.angle_max = 250

    def _steps(self,n_steps):
        for _ in range(n_steps):
            time.sleep(1./self.speed)
            self._step()
        

    def get_angle(self):
        return self.stepper._current_step/self.ratio*360

    def _step(self):
        self.stepper.step(direction=self.direction)


    def set_values(self,values):
        for io,val in zip(self.ios,values):
            io.value = bool(val)
    
    def stop(self):
        for io in self.ios:
            io.value = False

    def cmd(self,command,value):
        if command == 'home':
            if value == '1':
                self.go_home(fast=True)
            else:
                self.go_home()
            print('ok')
        elif command == 'go' and value and self.home_set:
            self.go_to_angle(int(value))
            print('ok')
        elif command == 'get':
            print('value:'+str(self.get_angle()))
        elif command == 'mode':
            if value == '0':
                self.set_mode('direct')
            elif value == '1':
                self.set_mode('forward')
            elif value == '2':
                self.set_mode('home_first')
            print('ok')
        elif command == 'speed':
            try:
                self.speed = int(value)
                print('ok')
            except ValueError:
                print('ko')
        else:
            print('ko')


    def go_to_angle(self,angle, mode = None):
        angle = min(angle,self.angle_max)
        angle = max(0,angle)
        if not mode:
            mode = self.mode
        if mode == 'direct':
            if (angle > self.get_angle()):
                self.direction = stepper.FORWARD
            else:
                self.direction = stepper.BACKWARD
            self._steps(abs(int(1.*angle/360*self.ratio)-self.stepper._current_step))
        elif mode == 'forward':
            steps_to_target = int(1.*angle/360*self.ratio)-self.stepper._current_step
            steps_backward = min(self.steps_backward,int(1.*angle/360*self.ratio))
            # if angle is greater than current value, go forward
            if steps_to_target>0:
                self.direction = stepper.FORWARD
                self._steps(abs(steps_to_target))
            # if angle is lower than current value, go backward a bit more,
            # then go forward
            else:
                self.direction = stepper.BACKWARD
                self._steps(steps_backward+abs(steps_to_target))
                self.direction = stepper.FORWARD
                self._steps(steps_backward)
        elif mode == 'home_first':
            self.go_home(fast=True)
            self.direction = stepper.FORWARD
            self._steps(int(1.*angle/360*self.ratio))
        self.stepper.release()

    def set_mode(self,mode):
        if mode in ['direct','forward','home_first']:
            self.mode = mode