import serial, time
PAUSE = 0.1

class Supervisor():
    '''
    Set a long timeout for devices requiring time to perform  the desired operation.
    '''
    def __init__(self, port = '/dev/ttyACM0', baudrate=115200, timeout=0.01):
        self.serial =  serial.Serial(port, baudrate=baudrate, timeout=timeout)
        self.timeout = timeout

    def _get_serial(self,timeout):
        t0 = time.time()
        buffer = ''
        while True:
            #print(buffer)
            buffer += ''.join([s.decode() for s in self.serial.readlines()])
            if ('ok\r' in buffer):
                print('Command successfull.')
                return True
            elif ('ko\r' in buffer):
                print('Error returned.')
                return False
            elif ('value:' in buffer):
                ret = buffer.split('value:')[-1].strip()
                print(f'Received value: {ret}')
                return ret
            elif ((time.time() - t0) > timeout):
                print('Timeout reached. No value returned.')
                return False


    def _send_cmd(self,cmd,timeout = 0.1):
        self.serial.write(str.encode(cmd+'\r'))
        time.sleep(PAUSE)
        return self._get_serial(timeout=timeout)


    def close(self):
        self.serial.close()

class Rotator(Supervisor):

    def __init__(self,*args,**kwargs):
        super(Rotator, self).__init__(*args, **kwargs)
        self.modes = {'direct': 0,'forward':1,'home_first':2}

    def home(self,fast = False, timeout = 60):
        print('Finding home position...')
        cmd = 'rotator home'
        if fast:
            cmd = ' '.join([cmd,'1'])
        self._send_cmd(cmd, timeout = timeout)

    def go_to(self,angle, timeout = 60):
        print(f'Going to angle={angle}...')
        cmd = f'rotator go {angle}'
        self._send_cmd(cmd, timeout = timeout)
    
    def get_angle(self):
        cmd = f'rotator get '
        return float(self._send_cmd(cmd))
        
    def set_speed(self,speed):
        cmd = f'rotator speed {speed}'
        self._send_cmd(cmd)

    def set_mode(self,mode):
        mode_id = self.modes.get(mode,None)
        if mode_id is not None:
            cmd = f'rotator mode {mode_id}'
            print(cmd)
            self._send_cmd(cmd)
        else:
            raise ValueError('Mode not recognized.')
            


class Shutter(Supervisor):

    def set_pos(self,name,value):
        cmd = f'shutter set {name}:{value}'
        self._send_cmd(cmd)

    def go_to(self,value):
        '''
        value can me name of a registered position or a angle value
        '''
        cmd = f'shutter go {value}'
        self._send_cmd(cmd)



## Rotator example
# rot = Rotator(port = '/dev/ttyACM7')
# rot.home(fast = True)
# rot.set_mode('forward')
# rot.go_to(20)
# print(rot.get_angle())
# rot.set_speed(100)
# rot.go_to(10)
# print(rot.get_angle())
# rot.close()

## Shutter example
# shutter = Shutter(port = '/dev/ttyACM0')
# shutter.go_to(0)
# time.sleep(0.5)
# shutter.set_pos('open',45)
# shutter.go_to('open')
# time.sleep(0.5)
# shutter.go_to(22.5)
# shutter.close()

