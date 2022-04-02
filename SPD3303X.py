from SCPI import SCPI

class SPD3303X:
    """
    Class for interacting with the SPD3303 Siglent Power Supply
    """

    class SPD3303Exception(Exception):
        '''
        Exception raised when a call returns an error message
        '''
        def __init__(self, code, message):
            self.code = code
            self.message = message
            super().__init__(self.message)

        def __str__(self):
            return f'Error Code: {self.code} -> {self.message}'
            

    scpi = None
    channel_count = 2
    save_file_count = 5
    INDEPENDENT_MODE = 0
    SERIES_MODE = 1
    PARALLEL_MODE = 2
    manufacturer = ""
    product_type = ""
    series_number = ""
    software_version = ""
    hardware_version = ""

    def __get_product_info(self):
        '''
        Query the manufacturer, product type, series, series no., software version, hardware version
        '''
        self.scpi.send("*IDN?")
        response = self.scpi.recv()
        resp_arr = response.split(",")
        self.manufacturer = resp_arr[0]
        self.product_type = resp_arr[1]
        self.series_number = resp_arr[2]
        self.software_version = resp_arr[3]
        self.hardware_version = resp_arr[4]

    def __send_cmd(self, cmd):
        '''
        Generic call to send command with error checking
        '''
        self.scpi.send(cmd)
        # Check for an error in regards to that command
        self.check_error()

    def save(self, file_num):
        '''
        Save the current state into non-volatile memory
        '''
        if file_num not in range(1,self.save_file_count+1):
            raise self.SPD3303Exception('20', f'Save file must be an integer 1 - {self.save_file_count}')
        else:
            self.scpi.send(f"*SAV {file_num}")

    def recall(self, file_num):
        '''
        Recall state that had been saved from nonvolatile memory
        '''
        if file_num not in range(1,self.save_file_count+1):
            raise self.SPD3303Exception('20', f'Save file must be an integer 1 - {self.save_file_count}')
        else:
            self.scpi.send(f"*RCL {file_num}")

    def select_channel(self, channel):
        '''
        Select the channel to be operated on
        '''
        if channel not in range(1,self.channel_count+1):
            raise self.SPD3303Exception('21', f'Channel # must be an integer 1 - {self.channel_count}')
        else:
            self.scpi.send(f"INSTrument CH{channel}")

    def get_active_channel(self):
        '''
        Query for the active channel
        '''
        self.scpi.send("INSTrument?")
        return self.scpi.recv()

    def get_current(self, channel):
        '''
        Get the current value for a given channel
        '''
        if channel not in range(1,self.channel_count+1):
            raise self.SPD3303Exception('21', f'Channel # must be an integer 1 - {self.channel_count}')
        else:
            self.scpi.send(f"MEASure:CURRent? CH{channel}")
            return float(self.scpi.recv())

    def get_voltage(self, channel):
        '''
        Get the voltage value for a given channel
        '''
        if channel not in range(1,self.channel_count+1):
            raise self.SPD3303Exception('21', f'Channel # must be an integer 1 - {self.channel_count}')
        else:
            self.scpi.send(f"MEASure:VOLTage? CH{channel}")
            return float(self.scpi.recv())

    def get_power(self, channel):
        '''
        Get the power value for a given channel
        '''
        if channel not in range(1,self.channel_count+1):
            raise self.SPD3303Exception('21', f'Channel # must be an integer 1 - {self.channel_count}')
        else:
            self.scpi.send(f"MEASure:POWEr? CH{channel}")
            return float(self.scpi.recv())

    def set_current(self, channel, value):
        '''
        Set the current value for the selected channel
        '''
        if channel not in range(1,self.channel_count+1):
            raise self.SPD3303Exception('21', f'Channel # must be an integer 1 - {self.channel_count}')
        else:
            self.__send_cmd(f"CH{channel}:CURRent {value}")
    
    def get_set_current(self, channel):
        '''
        Get the set current value of the channel
        '''
        if channel not in range(1,self.channel_count+1):
            raise self.SPD3303Exception('21', f'Channel # must be an integer 1 - {self.channel_count}')
        else:
            self.scpi.send(f"CH{channel}:CURRent?")

    def set_voltage(self, channel, value):
        '''
        Set the voltage value for the selected channel
        '''
        if channel not in range(1,self.channel_count+1):
            raise self.SPD3303Exception('21', f'Channel # must be an integer 1 - {self.channel_count}')
        else:
            self.__send_cmd(f"CH{channel}:VOLTage {value}")
    
    def get_set_voltage(self, channel):
        '''
        Get the set voltage value of the channel
        '''
        if channel not in range(1,self.channel_count+1):
            raise self.SPD3303Exception('21', f'Channel # must be an integer 1 - {self.channel_count}')
        else:
            self.scpi.send(f"CH{channel}:VOLTage?")

    def output_on(self, channel):
        '''
        Turn on the channel output
        '''
        if channel not in range(1,self.channel_count+1):
            raise self.SPD3303Exception('21', f'Channel # must be an integer 1 - {self.channel_count}')
        else:
            self.scpi.send(f"OUTPut CH{channel},ON")

    def output_off(self, channel):
        '''
        Turn off the channel output
        '''
        if channel not in range(1,self.channel_count+1):
            raise self.SPD3303Exception('21', f'Channel # must be an integer 1 - {self.channel_count}')
        else:
            self.scpi.send(f"OUTPut CH{channel},OFF")

    def set_operation_mode(self, mode):
        if mode == 0 or mode == 1 or mode == 2:
            self.scpi.send(f"OUTPut:TRACK {mode}")
        else:
            raise self.SPD3303Exception('22', f'Invalid Operation Mode')

    def turn_on_waveform_display(self, channel):
        '''
        Turn on the Waveform Display function of specified channel
        '''
        if channel not in range(1,self.channel_count+1):
            raise self.SPD3303Exception('21', f'Channel # must be an integer 1 - {self.channel_count}')
        else:
            self.__send_cmd(f"OUTPut:WAVE CH{channel},ON")

    def turn_off_waveform_display(self, channel):
        '''
        Turn on the Waveform Display function of specified channel
        '''
        if channel not in range(1,self.channel_count+1):
            raise self.SPD3303Exception('21', f'Channel # must be an integer 1 - {self.channel_count}')
        else:
            self.scpi.send(f"OUTPut:WAVE CH{channel},OFF")

    def set_timing_parameters(self, channel, group, voltage, current, time):
        '''
        Set the timing parameters of specified channel, group setting the voltage current and execution time
        '''
        if channel not in range(1,self.channel_count+1):
            raise self.SPD3303Exception('21', f'Channel # must be an integer 1 - {self.channel_count}')
        else:
            self.scpi.send(f"TIMEr:SET CH{channel},{group},{voltage},{current},{time}")

    def query_timing_parameters(self, channel, group):
        '''
        Query for the voltage/current/time parameters of specified group of specific channels
        '''
        if channel not in range(1,self.channel_count+1):
            raise self.SPD3303Exception('21', f'Channel # must be an integer 1 - {self.channel_count}')
        else:
            self.scpi.send(f"TIMEr:SET? CH{channel},{group}")
            response = self.scpi.recv()
            resp_arr = response.split(",")
            return (resp_arr[0],(resp_arr[1],resp_arr[2]))

    def turn_on_timer(self, channel):
        '''
        Turn on timer fuction of specific channel
        '''
        if channel not in range(1,self.channel_count+1):
            raise self.SPD3303Exception('21', f'Channel # must be an integer 1 - {self.channel_count}')
        else:
            self.scpi.send(f"TIMEr CH{channel},ON")

    def turn_off_timer(self, channel):
        '''
        Turn off timer fuction of specific channel
        '''
        if channel not in range(1,self.channel_count+1):
            raise self.SPD3303Exception('21', f'Channel # must be an integer 1 - {self.channel_count}')
        else:
            self.scpi.send(f"TIMEr CH{channel},OFF")

    def check_error(self):
        '''
        Check for an error on the system
        '''
        self.scpi.send("SYSTem:ERRor?")
        response = self.scpi.recv()
        resp_list = response.split('  ')
        # If error code zero do not raise exception, move along
        if resp_list[0] == '0':
            return False
        # Remove the newline at the end of the message
        resp_list[1] = resp_list[1][:-1]
        # Raise a response with the error code and message
        raise self.SPD3303Exception(resp_list[0], resp_list[1])

    def check_version(self):
        '''
        Query the software version of the equipment
        '''
        self.scpi.send("SYSTem:VERSion?")
        return self.scpi.recv()

    def check_status(self):
        '''
        Return the top level info about the power supply functional status
        '''
        self.scpi.send("SYSTem:STATus?")
        return self.scpi.recv()

    def assign_ip_addr(self, ip):
        '''
        Assign a static Internet Protocol (IP) address for the instrument
        WARING: This command is invalid when DHCP is on
        '''
        self.__send_cmd(f"IPaddr {ip}")

    def query_ip_addr(self):
        '''
        Query the static Internet Protocol (IP) address for the instrument
        '''
        self.scpi.send(f"IPaddr?")
        return self.scpi.recv()

    def assign_subnet_mask(self, subnet_mask):
        '''
        Assign a subnet mask for the instrument
        WARING: This command is invalid when DHCP is on
        '''
        self.__send_cmd(f"MASKaddr {subnet_mask}")

    def query_subnet_mask(self):
        '''
        Query the subnet mask for the instrument
        '''
        self.scpi.send(f"MASKaddr?")
        return self.scpi.recv()

    def assign_gate_address(self, gate_addr):
        '''
        Assign a gate address for the instrument
        WARING: This command is invalid when DHCP is on
        '''
        self.__send_cmd(f"GATEaddr {gate_addr}")

    def query_subnet_mask(self):
        '''
        Query the gate address for the instrument
        WARING: This command is invalid when DHCP is on
        '''
        self.scpi.send(f"GATEaddr?")
        return self.scpi.recv()
    
    def dhcp(self, state):
        '''
        Turn on or off DHCP
        '''
        if state:
            self.scpi.send(f"DHCP ON")
        else:
            self.scpi.send(f"DHCP OFF")

    def query_dhcp(self):
        '''
        Query to see the status of DHCP
        '''
        self.scpi.send(f"DHCP?")
        return self.scpi.recv()

    def close(self):
        '''
        Close the socket connection
        '''
        self.scpi.close()

    def __init__(self, ip):
        '''
        Init the SCPI connection and get the basic product info
        '''
        self.scpi = SCPI(ip, 5025)
        self.__get_product_info()
            