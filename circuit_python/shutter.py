import pulseio


class Shutter():
    def __init__(self,pin):
        self.pin = pin
        self.pwm = pulseio.PWMOut(pin, frequency=50, duty_cycle=0)
        # max duty cycle = 2**16
        self.min_pwm = 2500
        self.max_pwm = 7900
        self.pos = {'min':self.min_pwm, 'max':self.max_pwm}

    def cmd(self,command,value):
        if command == 'set':
            res = value.split(':')
            if len(res) == 2:
                self.register_position(res[0],int(res[1]))
                print('ok')
            else:
                print('ko')
        elif command == 'go':
            if value in self.pos:
                self.go_to_pos(value)
                print('ok')
            else:
                try:
                    angle = float(value)
                    self.go_to_angle(angle)
                    print('ok')
                except ValueError:
                    print('ko')
        else:
            print('ko')

    def angle_to_duty(self,angle):
        return int(float(angle)/180*(self.max_pwm-self.min_pwm)+self.min_pwm)

    def register_position(self,position,angle):
        self.pos[position] = self.angle_to_duty(angle)
        
    def go_to_angle(self,angle):
        self.pwm.duty_cycle = self.angle_to_duty(angle)

    def go_to_pos(self,position):
        value = self.pos.get(position,None)
        if value:
            self.pwm.duty_cycle = value
