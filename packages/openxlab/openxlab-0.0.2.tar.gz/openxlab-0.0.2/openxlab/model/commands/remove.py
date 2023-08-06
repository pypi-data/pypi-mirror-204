"""
delete model repository-cli
"""
from openxlab.types.command_type import *


class Remove(BaseCommand):
    """remove"""

    def get_name(self) -> str:
        return "remove"

    def add_arguments(self, parser: ArgumentParser) -> None:
        pass

    def take_action(self, parsed_args: Namespace) -> int:
        print("model repo remove")
        return 0
