from openxlab.types.command_type import *
from openxlab.model.commands.download import Download
from openxlab.model.commands.upload import Upload
from openxlab.model.commands.init import Init
from openxlab.model.commands.create import Create


class Model(BaseCommand):
    """model"""

    sub_command_list = [Upload, Download, Init, Create]

    def get_name(self) -> str:
        return "model"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "--foo",
            type=str,
            help=(
                "this is an argument for test"
            ),
        )

    def take_action(self, parsed_args: Namespace) -> int:
        pass
