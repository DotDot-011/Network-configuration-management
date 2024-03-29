from enum import Enum

class AvailableDevice(str, Enum):

    def __str__(self):
        return str(self.value)

    cisco = "cisco_ios"
    dell = "dell_os6"
    huawei = "huawei"
    zyxel = "zyxel_os"
