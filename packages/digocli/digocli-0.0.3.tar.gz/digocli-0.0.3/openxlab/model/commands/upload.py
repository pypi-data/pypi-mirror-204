"""
upload model file|meta file|log file|readme file-cli
"""
from openxlab.types.command_type import *


class Upload(BaseCommand):
    """upload"""

    def get_name(self) -> str:
        return "upload"

    def add_arguments(self, parser: ArgumentParser) -> None:
        pass

    def take_action(self, parsed_args: Namespace) -> int:
        print("upload something")
        return 0
