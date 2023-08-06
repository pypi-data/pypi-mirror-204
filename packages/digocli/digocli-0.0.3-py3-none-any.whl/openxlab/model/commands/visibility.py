"""
setting model repository visibility-cli
"""
from openxlab.types.command_type import *


class Visibility(BaseCommand):
    """visibility"""

    def get_name(self) -> str:
        return "visibility"

    def add_arguments(self, parser: ArgumentParser) -> None:
        pass

    def take_action(self, parsed_args: Namespace) -> int:
        print("change visibility")
        return 0
