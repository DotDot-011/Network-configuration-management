from enum import Enum


class CiscoCommand(str, Enum):

    def __str__(self):
        return str(self.value)

    showrun: str = "show run"
    showstart: str = "show startup-config"
    copy_run_to_start: str = "copy running-config startup-config"
    copy_start_to_run: str = "copy startup-config running-config"

class HuaweiCommand(str, Enum):

    def __str__(self):
        return str(self.value)

    showrun: str = "display current-configuration"
    copy_run_to_start: str = "save"

class DellCommand(CiscoCommand):
    
    pass
class ZyxelCommand(CiscoCommand):

    pass