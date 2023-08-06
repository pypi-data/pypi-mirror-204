"""
create model repository-cli
"""
from openxlab.types.command_type import *


class Create(BaseCommand):
    """create"""

    def get_name(self) -> str:
        return "create"

    def add_arguments(self, parser: ArgumentParser) -> None:
        pass

    def take_action(self, parsed_args: Namespace) -> int:
        print("create something")
        return 0
