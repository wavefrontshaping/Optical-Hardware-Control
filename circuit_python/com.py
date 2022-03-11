import supervisor

class Com():
    def __init__(self):
        self.devices = {}

    def register_device(self, name, callback):
        self.devices[name] = callback

    def wait_for_cmd(self):
        while True:
            if supervisor.runtime.serial_bytes_available:
                input_text = input().strip().split(' ')
                if len(input_text) > 1:
                    device_name = input_text[0]
                    if device_name in self.devices.keys():
                        cmd = input_text[1]
                        if len(input_text) > 2:
                            value = input_text[2]
                        else:
                            value = None
                        self.devices[device_name](cmd, value)
                    else:
                        print('ko')
