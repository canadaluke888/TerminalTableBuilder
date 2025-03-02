from rich.panel import Panel
from rich.console import Console

class SystemMessage:
    def __init__(self, console: Console):
        """
        Initialize main console.

        :param console: Rich Console for displaying system messages.
        """
        self.console = console

    def create_information_message(self, message: str) -> Panel:
        """
        Create a custom informational message from the system.

        Args:
            message (str): The message to display.

        Returns:
            Panel: The rendered panel with the message.
        """
        self.console.print(
            Panel(
                f"[bold yellow]{message}[/]",
                title="[bold green]Information[/]",
                title_align="center",
                border_style="white",
            )
        )

    def create_error_message(self, message: str) -> Panel:
        """
        Create a custom error message from the system.

        Args:
            message (str): The message and, optionally, error you want to display.

        Returns:
            Panel: The rendered panel with the message.
        """
        self.console.print(
            Panel(
                f"[bold red]{message}[/]",
                title="[bold red]Error[/]",
                title_align="center",
                border_style="white",
            )
        )

