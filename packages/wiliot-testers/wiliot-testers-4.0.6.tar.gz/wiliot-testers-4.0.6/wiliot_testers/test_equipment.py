"""
  Copyright (c) 2016- 2023, Wiliot Ltd. All rights reserved.

  Redistribution and use of the Software in source and binary forms, with or without modification,
   are permitted provided that the following conditions are met:

     1. Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.

     2. Redistributions in binary form, except as used in conjunction with
     Wiliot's Pixel in a product or a Software update for such product, must reproduce
     the above copyright notice, this list of conditions and the following disclaimer in
     the documentation and/or other materials provided with the distribution.

     3. Neither the name nor logo of Wiliot, nor the names of the Software's contributors,
     may be used to endorse or promote products or services derived from this Software,
     without specific prior written permission.

     4. This Software, with or without modification, must only be used in conjunction
     with Wiliot's Pixel or with Wiliot's cloud service.

     5. If any Software is provided in binary form under this license, you must not
     do any of the following:
     (a) modify, adapt, translate, or create a derivative work of the Software; or
     (b) reverse engineer, decompile, disassemble, decrypt, or otherwise attempt to
     discover the source code or non-literal aspects (such as the underlying structure,
     sequence, organization, ideas, or algorithms) of the Software.

     6. If you create a derivative work and/or improvement of any Software, you hereby
     irrevocably grant each of Wiliot and its corporate affiliates a worldwide, non-exclusive,
     royalty-free, fully paid-up, perpetual, irrevocable, assignable, sublicensable
     right and license to reproduce, use, make, have made, import, distribute, sell,
     offer for sale, create derivative works of, modify, translate, publicly perform
     and display, and otherwise commercially exploit such derivative works and improvements
     (as applicable) in conjunction with Wiliot's products and services.

     7. You represent and warrant that you are not a resident of (and will not use the
     Software in) a country that the U.S. government has embargoed for use of the Software,
     nor are you named on the U.S. Treasury Department’s list of Specially Designated
     Nationals or any other applicable trade sanctioning regulations of any jurisdiction.
     You must not transfer, export, re-export, import, re-import or divert the Software
     in violation of any export or re-export control laws and regulations (such as the
     United States' ITAR, EAR, and OFAC regulations), as well as any applicable import
     and use restrictions, all as then in effect

   THIS SOFTWARE IS PROVIDED BY WILIOT "AS IS" AND "AS AVAILABLE", AND ANY EXPRESS
   OR IMPLIED WARRANTIES OR CONDITIONS, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED
   WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, NONINFRINGEMENT,
   QUIET POSSESSION, FITNESS FOR A PARTICULAR PURPOSE, AND TITLE, ARE DISCLAIMED.
   IN NO EVENT SHALL WILIOT, ANY OF ITS CORPORATE AFFILIATES OR LICENSORS, AND/OR
   ANY CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
   OR CONSEQUENTIAL DAMAGES, FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES,
   FOR ANY LOSS OF USE OR DATA OR BUSINESS INTERRUPTION, AND/OR FOR ANY ECONOMIC LOSS
   (SUCH AS LOST PROFITS, REVENUE, ANTICIPATED SAVINGS). THE FOREGOING SHALL APPLY:
   (A) HOWEVER CAUSED AND REGARDLESS OF THE THEORY OR BASIS LIABILITY, WHETHER IN
   CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE);
   (B) EVEN IF ANYONE IS ADVISED OF THE POSSIBILITY OF ANY DAMAGES, LOSSES, OR COSTS; AND
   (C) EVEN IF ANY REMEDY FAILS OF ITS ESSENTIAL PURPOSE.
"""
from time import time, sleep
from statistics import mode
import sys
import serial
import serial.tools.list_ports
from yoctopuce.yocto_temperature import YAPI, YRefParam, YTemperature
import os


class EquipmentError(Exception):

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        # print('calling str')
        if self.message:
            return 'EquipmentError: {msg}'.format(msg=self.message)
        else:
            return 'EquipmentError has been raised'


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    available_ports = [s.device for s in serial.tools.list_ports.comports()]
    if len(available_ports) == 0:
        available_ports = [s.name for s in serial.tools.list_ports.comports()]
        if len(available_ports) == 0:
            print("no serial ports were found. please check your connections")
    return available_ports


class Attenuator(object):
    '''
    Support all attn classes for:
    '''

    def __init__(self, ATTN_type, comport='AUTO'):
        if 'MCDI-USB' in ATTN_type:
            self._active_TE = Attenuator.MCDI_USB()
        elif 'MCDI' in ATTN_type:
            self._active_TE = Attenuator.MCDI()
        elif 'API' in ATTN_type or 'Weinschel' in ATTN_type:
            self._active_TE = Attenuator.API(comport)

        else:
            pass

    def GetActiveTE(self):
        return self._active_TE

    class MCDI(object):

        def __init__(self):
            dotnet = False
            utils_dir = os.path.join(os.path.dirname(__file__), 'utils')
            sys.path.append(utils_dir)
            if dotnet == True:
                import clr  # pythonnet, manually installed with a downloaded wheel and pip
                import ctypes  # module to open utils files
                clr.AddReference("System.IO")
                import System.IO
                System.IO.Directory.SetCurrentDirectory(utils_dir)
                clr.AddReference('mcl_RUDAT_NET45')
                from mcl_RUDAT_NET45 import USB_RUDAT
                self.Device = USB_RUDAT()
                self.Device.Connect()
                info = self.DeviceInfo()
                print('Found Attenuator: Model {}, {} ,{} '.format(info[0], info[1], info[2]))
            else:
                from USB_RUDAT import USBDAT
                self.Device = USBDAT()
                info = self.DeviceInfo()
                print('Found Attenuator: Model {}, {} ,{} '.format(info[0], info[1], info[2]))

        def DeviceInfo(self):
            cmd = ":MN?"
            model_name = self.Device.Send_SCPI(cmd, "")
            cmd = ":SN?"
            serial = self.Device.Send_SCPI(cmd, "")
            cmd = ":FIRMWARE?"
            fw = self.Device.Send_SCPI(cmd, "")
            # return [model_name[1], serial[1], fw[1]]  #dotnet
            return [model_name, serial, fw]

        def Setattn(self, attn):
            cmd = ":SETATT:" + str(attn)
            status = int(self.Device.Send_SCPI(cmd, ""))
            if status == 0:
                print('Command failed or invalid attenuation set')
            elif status == 1:
                # print('Command completed successfully')
                print('Attenuation set to  {}[dB]'.format(float(self.Getattn())))
            elif status == 2:
                print(
                    'Requested attenuation was higher than the allowed range, the attenuation was set to the device�s maximum allowed value')
            # print(status)

        def Getattn(self):
            cmd = ":ATT?"
            Resp = float(self.Device.Send_SCPI(cmd, ""))
            # print(Resp)
            # if status == 0:
            #     print('Command failed or invalid attenuation set')
            # elif status == 1:
            #     print('Command completed successfully')
            return Resp

    class MCDI_USB(object):
        # 64 bit array to send to USB
        cmd1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0]  # 64 bit array to send to USB

        def __init__(self):
            # find the device
            self.dev = usb.core.find(idVendor=0x20ce, idProduct=0x0023)
            # was it found?
            if self.dev is None:
                raise ValueError('Device not found')
            # set the active configuration. with no args we use first config.
            #  for Linux only
            if sys.platform == 'linux':

                for configuration in self.dev:
                    for interface in configuration:
                        ifnum = interface.bInterfaceNumber
                    if not self.dev.is_kernel_driver_active(ifnum):
                        continue
                    try:
                        # print "detach kernel driver from device %s: interface %s" % (dev, ifnum)
                        self.dev.detach_kernel_driver(ifnum)
                    except usb.core.USBError:
                        pass

            self.dev.set_configuration()
            self.cmd1[0] = 41
            self.dev.write(0x01, self.cmd1)  # SN
            s = self.dev.read(0x81, 64)
            self.SerialNumber = ""
            i = 1
            while (s[i] > 0):
                self.SerialNumber = self.SerialNumber + chr(s[i])
                i = i + 1
            self.cmd1[0] = 40
            self.dev.write(0x01, self.cmd1)  # Model
            s = self.dev.read(0x81, 64)
            self.ModelName = ""
            i = 1
            while (s[i] > 0):
                self.ModelName = self.ModelName + chr(s[i])
                i = i + 1

            self.Maximum_Attn = float(self.ModelName[11:])
            self.cmd1[0] = 99
            self.dev.write(0x01, self.cmd1)  # FW
            s = self.dev.read(0x81, 64)
            self.FW = ""
            self.FW = chr(s[5]) + chr(s[6])
            self.status_message = 'Found Attenuator: Model {}, SN: {} , FW: {}, Maximum attenuation: {}dB '.format(
                str(self.ModelName), str(self.SerialNumber), str(self.FW), str(self.Maximum_Attn))
            print(self.status_message)

        def ReadSN(self):
            return str(self.SerialNumber)

        def ReadMN(self):
            return str(self.ModelName)

        def ReadFW(self):
            return str(self.FW)

        def ReadMaxRange(self):
            return self.Maximum_Attn

        def Setattn(self, Attn):
            self.cmd1[0] = 19
            self.cmd1[1] = int(Attn)
            self.cmd1[2] = int((Attn - int(Attn)) * 4)
            if Attn > self.Maximum_Attn:
                print('Attenuation not in Range,setting maximum = {} '.format(str(self.Maximum_Attn)))
                self.cmd1[1] = int(self.Maximum_Attn)
                self.cmd1[2] = int((self.Maximum_Attn - int(self.Maximum_Attn)) * 4)
            # self.dev.set_configuration()

            try:
                self.dev.write(0x01, self.cmd1)  # Set attenuation
                s = self.dev.read(0x81, 64)
                self.new_att = 'Setting Attenuation = {}dB '.format(str(s[1] + s[2] / 4))
                print(self.new_att)
                return s[1] + s[2] / 4
            except Exception as e:
                print(e)
                self.new_att = e
                return s

        def Getattn(self):
            # self.dev.set_configuration()
            try:
                self.cmd1[0] = 18
                self.dev.write(0x01, self.cmd1)  # Get attenuattion
                s = self.dev.read(0x81, 64)
                self.new_att = 'Current Attenuation = {}dB '.format(str(s[1] + s[2] / 4))
                print(self.new_att)
                return s[1] + s[2] / 4
            except Exception as e:
                print(e)
                self.new_att = e
                return s

        def Send_SCPI(self, SCPIcmd, tmp):
            # send SCPI commands (to supported firmware only!)
            self.cmd1[0] = 42
            l1 = 0
            l1 = len(SCPIcmd)
            indx = 1
            while (indx <= l1):
                self.cmd1[indx] = ord(SCPIcmd[indx - 1])
                indx = indx + 1
            self.cmd1[indx] = 0
            self.dev.write(0x01, self.cmd1)  # SCP Command up to 60 chars;
            s = self.dev.read(0x81, 64)
            i = 1
            RetStr = ""
            while (s[i] > 0):
                RetStr = RetStr + chr(s[i])
                i = i + 1
            return str(RetStr)

    class API(object):

        def __init__(self, comport="AUTO"):
            self.baudrate = 9600
            if comport == "AUTO":
                ports_list = serial_ports()
                for port in ports_list:
                    self.comport = port
                    self.s = serial.Serial(self.comport, self.baudrate, timeout=0.5)
                    sleep(1)
                    self.s.flushInput()
                    self.s.flushOutput()
                    sleep(0.1)
                    # Turn the console off
                    self.s.write("CONSOLE DISABLE\r\n".encode())
                    # Flush the buffers
                    sleep(0.1)
                    self.s.flush()
                    self.s.flushInput()
                    self.s.flushOutput()
                    self.s.write("*IDN?\r\n".encode())
                    sleep(0.1)
                    if self.s.in_waiting > 1:
                        resp = self.s.readline().decode("utf-8")
                    else:
                        resp = ''
                    self.model = resp
                    if ("Aeroflex" in resp):
                        print('Found ' + resp.strip('\r\n') + ' on port: ' + port)
                        break
                    elif '8311' in resp or '8331' in resp:
                        print('Found ' + resp.strip('\r\n') + ' on port: ' + port)
                    else:
                        pass
            else:
                self.s = serial.Serial(comport, self.baudrate, timeout=0.5)
                sleep(1)
                self.s.write("CONSOLE DISABLE\r\n".encode())
                # Flush the buffers
                self.s.flush()
                self.s.flushInput()
                self.s.flushOutput()
                self.Query("*IDN?\r\n")
                resp = self.Query("*IDN?\r\n")
                self.model = resp
                if ("Aeroflex" in resp) or ("4205" in resp):
                    print('Found ' + resp.strip('\r\n') + ' on port: ' + comport)
                elif '8311' in resp or '8331' in resp:
                    print('Found ' + resp.strip('\r\n') + ' on port: ' + comport)
                else:
                    self.close_port()
                    print('Aeroflex Attenuator not found on selected port, check connection', file=sys.stderr)

        def Write(self, cmd, wait=False):
            """Send the input cmd string via COM Socket"""
            if self.s.isOpen():
                pass
            else:
                self.s.open()
            self.s.flushInput()
            sleep(1)
            try:
                self.s.write(str.encode(cmd))
                sleep(0.1)  # Commands may be lost when writing too fast

            except:
                pass
            # self.s.close()

        def Query(self, cmd):
            """Send the input cmd string via COM Socket and return the reply string"""
            if self.s.isOpen():
                pass
            else:
                self.s.open()
                sleep(0.1)
            # self.s.flushInput()
            sleep(1)
            try:
                self.s.write(cmd.encode())
                sleep(0.1)
                if self.s.in_waiting > 0:
                    data = self.s.readline().decode("utf-8")
                else:
                    data = ''
            except:
                data = ''
            # self.s.close()
            return data

        def close_port(self):
            if self.s is not None and self.s.isOpen():
                self.s.close()

        def is_open(self, check_port=False):
            if self.s is not None:
                if check_port:
                    try:
                        self.Query("*IDN?\r\n")
                        resp = self.Query("*IDN?\r\n")
                        self.model = resp
                        if ("Aeroflex" in resp):
                            return True
                        elif '8311' in resp or '8331' in resp:
                            return True
                    except:
                        self.close_port()
                else:
                    return self.s.isOpen()
            return False

        def Setattn(self, attn):
            cmd = "ATTN {:.2f}\r\n".format(attn)
            self.Write(cmd)
            value = self.Getattn()
            value = float(value)
            if value != attn:
                print(f'Error setting attenuation: new : {attn} current: {value}')
            return value

        def Getattn(self):
            cmd = "ATTN?\r\n"
            value = self.Query(cmd)
            return value


class Tescom:
    """
    Control TESCOM testing chambers
    """
    open_cmd = b'OPEN\r'
    close_cmd = b'CLOSE\r'
    com_port_obj = None
    models_list = ['TC-5064C', 'TA-7011AP', 'TC-5063A', 'TC-5970CP']

    def __init__(self, port=None):
        self.port = port
        try:
            if port is not None:
                self.connect(port)

        except Exception as e:
            print(e)
            print("Tescom - Connection failed")

    def connect(self, port):
        """
        :param port: com port to connect
        :return: com port obj
        """
        try:
            com_port_obj = self.com_port_obj = serial.Serial(port=port, baudrate=9600, timeout=1)
            if com_port_obj is not None:
                self.door_cmd = None
                self.com_port_obj.write(b'MODEL?\r')
                sleep(0.1)
                model = str(self.com_port_obj.read(14))
                parts = [p for p in model.split("'")]
                parts = [p for p in parts[1].split(" ")]
                self.model = parts[0]
                if len(self.model) > 0:
                    print("RF chamber connected to port " + str(port))
                    print("Tescom - Chamber model:", self.model)
                else:
                    print("Tescom - Error! No chamber found")
                    return
                if self.model in self.models_list:
                    self.door_cmd = b'DOOR?\r'
                else:
                    self.door_cmd = b'LID?\r'
            else:
                raise Exception
        except Exception as e:
            # print(e)
            print(("Tescom - Could not connect to port " + port))
            return None

    def close_port(self):
        """
        closes com port
        """
        try:
            self.com_port_obj.close()
            print("RF chamber disconnected from port: " + str(self.port))
        except Exception as e:
            print("Could not disconnect")

    def open_chamber(self):
        """
        opens chamber
        :return: "OK" if command was successful
        """
        if self.is_door_open():
            print("Chamber is open")
            return 'OK'
        try:
            print(f"Chamber {self.port} is opening")
            self.com_port_obj.reset_input_buffer()
            self.com_port_obj.reset_output_buffer()
            self.com_port_obj.write(self.open_cmd)
            res = ''
            wait_counter = 0
            while 'OK' not in res:
                if wait_counter >= 15:
                    raise Exception(f"Error in opening chamber {self.port}")
                res = self.com_port_obj.read(14).decode(
                    'utf-8').upper().rstrip('\r')
                if len(str(res)) > 0:
                    print(f'Chamber {self.port} status: ' + str(res))
                wait_counter += 1
                sleep(0.1)
            if not self.is_door_open():
                raise Exception(
                    f"{self.port} Door status doesn't match command sent!")
            print(f"Chamber {self.port} is open")
            return 'OK'
        except Exception as e:
            print(e)
            return "FAIL"

    def close_chamber(self):
        """
        closes chamber
        :return: "OK" if command was successful
        """
        if self.is_door_closed():
            print("Chamber closed")
            return 'OK'
        try:
            print(f"CHAMBER {self.port} IS CLOSING, CLEAR HANDS!!!")
            sleep(2)
            self.com_port_obj.write(self.close_cmd)
            res = ''
            wait_counter = 0
            while 'READY' not in res:
                if wait_counter >= 20:
                    raise Exception(f"Error in closing chamber {self.port}")
                res = self.com_port_obj.read(14).decode(
                    'utf-8').upper().rstrip('\r')
                if 'ERR' in res or 'READY' in res or 'OK' in res:
                    print(f'Chamber {self.port} status: ' + str(res))
                if 'ERR' in res:
                    return "FAIL"
                wait_counter += 1
                sleep(0.1)
            if not self.is_door_closed():
                raise Exception(
                    f"{self.port} Door status doesn't match command sent!")
            print(f"Chamber {self.port} closed")
            return 'OK'
        except Exception as e:
            print(f"Error in closing chamber {self.port}")
            print(e)
            return "FAIL"

    def is_connected(self):
        if self.com_port_obj is None:
            return False
        return self.com_port_obj.isOpen()

    def get_state(self):
        self.com_port_obj.reset_input_buffer()
        sleep(0.1)
        self.com_port_obj.write(self.door_cmd)
        sleep(0.1)
        state = self.com_port_obj.read(14).decode('utf-8').upper().rstrip('\r')
        return state

    def is_door_open(self):
        state = self.get_state()
        if 'OPEN' in state:
            return True
        return False

    def is_door_closed(self):
        state = self.get_state()
        if 'CLOSE' in state:
            return True
        return False


class BarcodeScanner(object):
    prefix = '~0000@'
    suffix = ';'
    com = ''
    serial = None

    def __init__(self, com=None, baud=115200, config=True, log_type='NO_LOG'):
        self.log_type = log_type
        if com != None:
            self.open_port(com, baud=baud, config=config)
        # else:
        #     self.serial = ser = Serial()

    def open_port(self, com, baud=115200, config=True):
        if self.serial != None and self.serial.is_open():
            self.serial.closePort()
        self.serial = ser = serial.Serial(com, baud, timeout=0.5)
        if not self.check_com_port():
            print(f'{com} is not barcode scanner')
        if ser != None and self.log_type != 'NO_LOG':
            print(f'Barcode scanner ({com}) connected.')
        elif ser == None:
            print(f'Barcode scanner - Problem connecting {com}')
        self.com = com
        ser.timerout = 1  # read time out
        ser.writeTimeout = 0.5  # write time out.
        if config:
            self.configure()

    def find_and_open_port(self, baud=115200, config=True):
        com = self.find_com_port(baud)
        if com is not None:
            self.open_port(com, baud, config)
            return True
        return False

    def find_com_port(self, baud=115200):
        comPorts = serial_ports()
        coms = []
        for com in comPorts:
            if self.check_com_port(com, baud):
                coms.append(com)
                if len(coms) > 1:
                    print(
                        'Warning - more than one barcode scanner found, using the first barcode scanner.')

        if len(coms) > 0:
            return coms[0]
        else:
            print('Error - could not find barcode scanner.')
            return None

    def check_com_port(self, com=None, baud=115200):
        is_bar_scan = True
        close_port = False
        if not self.is_open() and com is not None:
            close_port = True
            self.serial = serial.Serial(com, baud, timeout=0.5)
        elif not self.is_open():
            print('BarcodeScanner - check_com_port: Missing com port')
            return False
        res = self.manual_configure(['QRYPDN'])
        if not 'NLS-N1' in str(res):
            is_bar_scan = False
        if close_port:
            self.serial.close()
            self.serial = None

        return is_bar_scan

    def close_port(self):
        if self.serial.isOpen():
            self.serial.close()

    def is_open(self):
        try:
            res = self.manual_configure(['QRYPDN'])
            if 'NLS-N1' in str(res):
                return True
            return False
        except:
            return False

    def configure(self, illScn='1', amlEna='0', grbEna='0', grbVll='2', atsEna='0', atsDur='36000', scnMod='0',
                  pwbEna='0'):
        '''
        illScn - illumination:    0-off, 1-normal, 2-always on
        amlEna - aiming:          0-off, 1-normal, 2-always on
        pwbEna - power on beep    0-off, 1-on
        grbEna - good read beep   0-off, 1-on
        atsEna - auto sleep       0-disable, 1-enable
        atsDur - sleep duration   1-36000 [sec]
        scnMod - scan mode        0-level mode, 2-sense mode, 3-continuous mode, 7-batch mode
        '''
        sleep(0.1)
        params = {'ILLSCN': illScn, 'AMLENA': amlEna, 'GRBENA': grbEna, 'ATSENA': atsEna,
                  'GRBVLL': grbVll, 'ATSDUR': atsDur, 'SCNMOD': scnMod, 'PWBENA': pwbEna}
        params = [key + value for key, value in params.items()]
        t, isSuccess = self.manual_configure(params)
        if isSuccess and self.log_type != 'NO_LOG':
            print(f'Barcode scanner ({self.com}) configured successfully.')
        elif not isSuccess:
            print(f'Barcode scanner ({self.com}) configuration failed.')

    def restore_all_factory_defaults(self):
        sleep(0.1)
        params = {'FACDEF': ''}
        params = [key + value for key, value in params.items()]
        t, isSuccess = self.manual_configure(params)
        if isSuccess and self.log_type != 'NO_LOG':
            print(f'Barcode scanner ({self.com}) restored factory default successfully.')
        elif not isSuccess:
            print(f'Barcode scanner ({self.com}) restored factory default failed.')

    def manual_configure(self, params):
        sleep(0.1)
        configs = self.prefix + ';'.join(params) + self.suffix
        self.serial.flushInput()
        self.serial.flushOutput()
        self.serial.write(str.encode(configs))
        sleep(0.1)
        t, isSuccess = self.trigger_stop_settings()
        # print(t)
        return t, isSuccess

    def scan(self):
        # print("analog_trigger_setting")
        self.serial.write(b"\x1b\x31")
        sleep(0.1)
        # t = ser.read(ser.in_waiting)
        t = self.serial.read_all()
        # print(t)
        return t

    def scan_and_flush(self):
        self.serial.flushInput()
        self.serial.flushOutput()
        t = self.scan()
        self.serial.flushInput()
        self.serial.flushOutput()
        tClean = str(t).split('\\x')[-1]
        if tClean.startswith('06'):
            tClean = tClean[2:]
            tClean = tClean.strip("'\\n\\r")
            tClean = tClean.split('\\n')[-1]
            tClean = tClean.split('\\r')[-1]
            return tClean
        else:
            print('Warning - not received ACK from barcode scanner.')
            return str(t).split('\\x')[-1]

    def scan_ext_id(self, scanDur=0.5, ValidateCnt=3):
        barcodeRead = ''
        barcodes = []
        startTime = time()
        while ((time() - startTime) < scanDur):
            barcodeRead = self.scan_and_flush()
            # barcodeRead = str(t)
            if len(barcodeRead) < 8:
                barcodeRead = ''
                continue

            if len(barcodes) < ValidateCnt:
                barcodes.append(barcodeRead)
                continue

            barcodeRead = mode(barcodes)
            fullData = curId = reelId = gtin = barcodeRead
            try:
                if ')' in fullData:
                    gtin = ')'.join(fullData.split(')')[:2]) + ')'
                    tagData = fullData.split(')')[2]
                else:  # gtin without parenthesis
                    gtin = fullData[0:18]
                    tagData = fullData[18:]
                curId = tagData.split('T')[1].strip("' ").split('(')[0]
                reelId = tagData.split('T')[0].strip("' ")
                return fullData, curId, reelId, gtin
            except:
                pass

            return fullData, curId, reelId, gtin

        return None, None, None, None

    def auto_scan(self):
        # print("Automatic reading settings")
        self.serial.write(b"\x1b\x32")
        sleep(0.1)
        t = self.serial.read_all()
        # print(t)
        return t

    def trigger_stop_settings(self):
        # print("Trigger_stop_settings")
        # sleep(0.1)
        # t = ser.read(ser.in_waiting)
        sleep(0.1)
        t = self.serial.read_all()
        sleep(0.1)
        # print(t)
        acks = str(t).split(';')[:-1]
        isSuccess = all([True if ack.endswith('\\x06')
                         else False for ack in acks])
        return t, isSuccess


class YoctoTemperatureSensor(object):
    def __init__(self):
        self.sensor = None
        errmsg = YRefParam()
        # Setup the API to use local USB devices
        if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
            raise EquipmentError('yocto temperature sensor got init error: {}'.format(errmsg.value))

    def connect(self, target='any'):
        if target == 'any':
            # retrieve any temperature sensor
            self.sensor = YTemperature.FirstTemperature()
        elif target == '':
            print('specified invalid target')
            return False
        else:
            self.sensor = YTemperature.FindTemperature(target + '.temperature')
        if self.sensor is None or self.get_sensor_name() == 'unresolved':
            print('No module connected')
            return False
        else:
            return True

    def get_sensor_name(self):
        if self.sensor is None:
            print('no sensor is connected. try to call connect() first')
            return ''

        sensor_str = self.sensor.describe()
        name_str = sensor_str.split('=')[1].split('.')[0]
        return name_str

    def get_temperature(self):
        if self.sensor is None:
            print('sensor is not connected. try to call connect() first')
            return float('nan')
        if not (self.sensor.isOnline()):
            print('sensor is not connected or disconnected during run')
            return float('nan')

        return self.sensor.get_currentValue()

    @staticmethod
    def exit_app():
        YAPI.FreeAPI()
