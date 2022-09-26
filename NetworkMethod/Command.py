from enum import Enum


class CiscoCommand(Enum):

    def __str__(self):
        return str(self.value)

    showrun: str = "show run"
    showstart: str = "show startup-config"
    copy_run_to_start: str = "copy running-config startup-config"
    copy_start_to_run: str = "copy startup-config running-config"