from pydantic import BaseModel
from utils.Enums import AvailableDevice
from NetworkMethod.Command import CiscoCommand, DellCommand, HuaweiCommand, ZyxelCommand
from netmiko import ConnectHandler
from netmiko.zyxel import ZyxelSSH

class AccessPointModel(BaseModel):

    device_type: AvailableDevice
    host: str
    username: str
    password: str
    port: int = 22
    secret: str = ''

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

    def UploadConfig(self, file):

        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            output = net_connect.send_config_from_file(file)

    def CopyRunToStartup(self):
    
        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            output = net_connect.send_command(CiscoCommand.copy_run_to_start.value)

class Huawei(AccessPointModel):
    
    def GetConfig(self):

        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            output = net_connect.send_command(HuaweiCommand.showrun.value)
    
        return output

    def UploadConfig(self, file):

        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            output = net_connect.send_config_from_file(file)

    def CopyRunToStartup(self):
    
        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            output = net_connect.send_command(HuaweiCommand.copy_run_to_start.value)

class Dell(AccessPointModel):
    
    def GetConfig(self):

        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            output = net_connect.send_command(DellCommand.showrun.value)
    
        return output

    def UploadConfig(self, file):

        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            output = net_connect.send_config_from_file(file)

    def CopyRunToStartup(self):
    
        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            output = net_connect.send_command(DellCommand.copy_run_to_start.value)

class Zyxel(AccessPointModel):
    
    def GetConfig(self):

        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            output = net_connect.send_command(ZyxelCommand.showrun.value)
    
        return output

    def UploadConfig(self, file):

        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            output = net_connect.send_config_from_file(file)

    def CopyRunToStartup(self):
    
        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            output = net_connect.send_command(ZyxelCommand.copy_run_to_start.value)