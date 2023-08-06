"""
model repository init-cli
"""
from openxlab.types.command_type import *
from openxlab.model.handler import download_metafile_template


class Init(BaseCommand):
    """init"""

    def get_name(self) -> str:
        return "init"

    def add_arguments(self, parser: ArgumentParser) -> None:
        pass

    def take_action(self, parsed_args: Namespace) -> int:
        download_metafile_template()
        return 0
