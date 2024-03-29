from pydantic import BaseModel
from utils.Enums import AvailableDevice
from NetworkMethod.Command import CiscoCommand, DellCommand, HuaweiCommand, ZyxelCommand
from netmiko import ConnectHandler
from netmiko.zyxel import ZyxelSSH
from pysnmp.hlapi import *
import logging

logging.basicConfig(filename='netmiko_global.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")

class AccessPointModel(BaseModel):

    device_type: AvailableDevice
    host: str
    username: str
    password: str
    port: int = 22
    secret: str = ''

    def __parse_to_device__(self):
        device = self.__dict__
        device['device_type'] = self.device_type
        return device

    def getDescr(self, community: str):
        
        iterator = getCmd(
            SnmpEngine(),
            CommunityData(community),
            UdpTransportTarget((self.host, 161)),
            ContextData(),
            ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0))
        )

        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

        if errorIndication:
            raise (errorIndication)

        elif errorStatus:
            raise ('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

        else:
            for varBind in varBinds:
                return str(varBind[1])

    def getUptime(self, community: str):
        
        iterator = getCmd(
            SnmpEngine(),
            CommunityData(community),
            UdpTransportTarget((self.host, 161)),
            ContextData(),
            ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysUpTime', 0))
        )

        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

        if errorIndication:
            raise (errorIndication)

        elif errorStatus:
            raise ('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

        else:
            for varBind in varBinds:
                return int(varBind[1])

    def getLocation(self, community: str):
        
        iterator = getCmd(
            SnmpEngine(),
            CommunityData(community),
            UdpTransportTarget((self.host, 161)),
            ContextData(),
            ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysLocation', 0))
        )

        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

        if errorIndication:
            raise (errorIndication)

        elif errorStatus:
            raise ('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

        else:
            for varBind in varBinds:
                return str(varBind[1])

class Cisco(AccessPointModel):

    def test(self):
        
        return "Good"

    def GetConfig(self):

        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            net_connect.enable()
            output = net_connect.send_command(CiscoCommand.showrun.value)
    
        return output

    def UploadConfig(self, commands):

        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            net_connect.enable()
            output = net_connect.send_config_set(commands)

    def CopyRunToStartup(self):
    
        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            net_connect.enable()
            output = net_connect.save_config()
    
    def EnableSnmp(self, community: str):
        
        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            net_connect.config_mode()
            output = net_connect.send_command(f'snmp-server community {community} RO')

        return output
    
    def getVersion(self):

        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            output = net_connect.send_command(CiscoCommand.showversion.value)
            
        return output

class Huawei(AccessPointModel):
    
    def GetConfig(self):

        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            net_connect.enable()
            output = net_connect.send_command(HuaweiCommand.showrun.value)
    
        return output

    def UploadConfig(self, commands):

        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            net_connect.enable()
            output = net_connect.send_config_set(commands)

    def CopyRunToStartup(self):
    
        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            net_connect.enable()
            output = net_connect.save_config()

class Dell(AccessPointModel):
    
    def GetConfig(self):

        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            net_connect.enable()
            output = net_connect.send_command(DellCommand.showrun.value)
    
        return output

    def UploadConfig(self, commands):

        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            net_connect.enable()
            output = net_connect.send_config_set(commands)

    def CopyRunToStartup(self):
    
        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            net_connect.enable()
            output = net_connect.save_config()

class Zyxel(AccessPointModel):
    
    def GetConfig(self):

        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            net_connect.enable()
            output = net_connect.send_command(ZyxelCommand.showrun.value)
    
        return output

    def UploadConfig(self, commands):

        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            net_connect.enable()
            output = net_connect.send_config_set(commands)

    def CopyRunToStartup(self):
    
        device = self.__parse_to_device__()
        with ConnectHandler(**device) as net_connect:
            net_connect.enable()
            output = net_connect.save_config()