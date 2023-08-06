"""
get model list of repository-cli
"""
from openxlab.types.command_type import *


class List(BaseCommand):
    """list"""

    def get_name(self) -> str:
        return "list"

    def add_arguments(self, parser: ArgumentParser) -> None:
        pass

    def take_action(self, parsed_args: Namespace) -> int:
        print("model list")
        return 0
