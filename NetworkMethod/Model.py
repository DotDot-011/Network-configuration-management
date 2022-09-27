from msilib.schema import File
from pydantic import BaseModel
from utils.Enums import AvailableDevice
from NetworkMethod.Command import CiscoCommand, HuaweiCommand
from netmiko import ConnectHandler
from netmiko.huawei.huawei import HuaweiSSH

class AccessPointModel(BaseModel):

    device_type: AvailableDevice
    host: str
    username: str
    password: str

    def __parse_to_device__(self):
        device = self.__dict__
        device['device_type'] = device['device_type'].value
        return device

class Cisco(AccessPointModel):

    def test(self):
        
        return "Good"

    def GetConfig(self):

        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            output = net_connect.send_command(CiscoCommand.showrun.value)
    
        return output

    def UploadConfig(self, file: File):

        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            output = net_connect.send_config_from_file(file)

    def CopyRunToStartup(self):
    
        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            output = net_connect.send_command(CiscoCommand.copy_run_to_start)

class Huawei(AccessPointModel):
    
    def GetConfig(self):

        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            output = net_connect.send_command(HuaweiCommand.showrun.value)
    
        return output

    def UploadConfig(self, file: File):

        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            output = net_connect.send_config_from_file(file)

    def CopyRunToStartup(self):
    
        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            output = net_connect.send_command(CiscoCommand.copy_run_to_start)