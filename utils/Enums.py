from enum import Enum

class AvailableDevice(Enum):

    def __str__(self):
        return str(self.value)

    cisco = "cisco_ios"
    dell = ""
    huawei = "huawei"
    zyxel = ""
