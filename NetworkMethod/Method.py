from msilib.schema import File
from netmiko import ConnectHandler
from NetworkMethod.Command import Command
from utils.NetworkModel import AccessPointModel

def GetConfig(access_point_config: AccessPointModel):

    with ConnectHandler(**access_point_config.__dict__) as net_connect:
        output = net_connect.send_command(Command.showrun.value)
    
    return output

def UploadConfig(access_point_config: AccessPointModel, file: File):

    with ConnectHandler(**access_point_config.__dict__) as net_connect:
        output = net_connect.send_config_from_file(file)

def CopyRunToStartup(access_point_config: AccessPointModel):
    
    with ConnectHandler(**access_point_config.__dict__) as net_connect:
        output = net_connect.send_command(Command.copy_run_to_start)