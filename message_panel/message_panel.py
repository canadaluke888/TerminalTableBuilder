from rich.panel import Panel
from functools import cache
from rich.console import Console

class MessagePanel:
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

    @staticmethod
    @cache
    def get_welcome_message() -> str:
        """
        Load and cache welcome static message data.
        """
        return """
[bold yellow]A terminal app where you can build and edit tables.[/]

[bold cyan]SQLite database supported![/]

[bold red]Type 'help' for instructions.[/]        
        """

    @staticmethod
    @cache
    def get_main_menu_instructions() -> str:
        """
        Load and cache static Main Menu instructions.
        """
        return """
[green]
- [bold cyan]table builder[/]: Enter the table builder.
- [bold cyan]settings[/]: Enter the settings.
- [bold cyan]exit[/]: Exit the application.
[/]
        """
        
    @staticmethod
    @cache
    def get_table_builder_instructions() -> str:
        """
        Load and cache static Table Builder instructions.
        """
        return """
[bold blue]Welcome to the Table Builder![/]

- [bold cyan]add column[/]: Add a column to the table.
- [bold cyan]change type[/]: Change the data type for a column.
- [bold cyan]rename column[/]: Change the name for one of the column headings.
- [bold cyan]add row[/]: Add a row to the table.
- [bold cyan]remove column[/]: Removes a column from the table.
- [bold cyan]remove row[/]: Removes a row from the table.
- [bold cyan]edit cell[/]: Allows you to edit the content of a cell in the table.
- [bold cyan]print table[/]: Prints the table to the screen.
- [bold cyan]rename[/]: Renames the table.
- [bold cyan]print table data[/]: Prints the JSON data for the table.
- [bold cyan]clear table[/]: Clears the table from memory.
- [bold cyan]load table[/]: Load a table from the database.
- [bold cyan]delete table[/]: Deletes the table from the database.
- [bold cyan]save table[/]: Save the table to the database or overwrite existing one.
- [bold cyan]current table[/]: Show the current working table.
- [bold cyan]load csv[/]: Loads a CSV file into a formatted table.
- [bold cyan]load csv batch[/]: Load a bunch of CSV files automatically from a directory into the database.
- [bold cyan]list tables[/]: List the available tables from the database.
- [bold cyan]save csv[/]: Save the data from the table to a CSV file.
- [bold cyan]save pdf[/]: Save the table to a PDF file.
- [bold cyan]save json[/]: Save the table data to a JSON file.
- [bold cyan]exit[/]: Go back to the main menu.
- [bold cyan]help[/]: Prints this screen.
        """
        
    @staticmethod
    @cache
    def get_settings_instructions() -> str:
        """
        Load and cache static Settings instructions.
        """
        return """
[bold yellow]Welcome to the Settings![/]

[bold yellow]Instructions:[/]
[green]
- Enter the setting and then the value.
- Use 'print settings' to show the current settings.
[/green]
[bold red]Tip:[/] Double-check your input for accuracy!
        """

    @staticmethod
    @cache
    def get_database_instructions() -> str:
        """
        Load and cache static Database Manager instructions.
        """
        return """
[bold yellow]Welcome to the Database Manager![/]

[green]
- [bold cyan]create database:[/] Create a new SQLite database and set it as the current database.
- [bold cyan]delete database:[/] Delete an existing SQLite database.
- [bold cyan]list databases:[/] List all databases in a specified directory.
- [bold cyan]select database:[/] Choose a database from a list of available databases.
- [bold cyan]current database:[/] Show the currently connected database.
- [bold cyan]close database:[/] Close the current database connection.
- [bold cyan]search:[/] Search through the current database based on a query. Returns information on the table, type, and position.
- [bold cyan]help:[/] Print this instruction screen.
- [bold cyan]exit:[/] Return to the main menu.
[/green]

[bold red]Tip:[/] Use [bold cyan]'select database'[/] to view and set a database. [bold cyan]'search'[/] to locate table data.
        """
        
                

    def print_welcome_message(self) -> Panel:
        """
        Print the welcome message upon login.
        
        Return: The rendered panel with the welcome message.
        """
        
        self.console.print(
            Panel(self.get_welcome_message(),
                title="[bold red]Terminal Table Builder[/]",
                subtitle="[bold white]Welcome![/]",
                subtitle_align="center",
                border_style="cyan",
            )
        )

    def print_main_menu_instructions(self) -> Panel:
        """
        Print the commands for the main menu.
        
        Return: The rendered panel with the instructions message.
        """
        self.console.print(
            Panel(self.get_main_menu_instructions(),
                title="[bold red]Main Menu[/] - [bold white]Instructions[/]",
                title_align="center",
                border_style="cyan",
            )
        )

    def print_table_builder_instructions(self) -> Panel:
        """
        Print the commands for the table builder portion of the app.
        
        Return: The rendered panel with the instructions message.
        """
        self.console.print(
            Panel(self.get_table_builder_instructions(),
                title="[bold red]Table Builder[/] - [bold white]Instructions[/]",
                title_align="center",
                border_style="cyan",
            )
        )

    def print_settings_instructions(self) -> Panel:
        """
        Print the commands for the settings.
        
        Return: The rendered panel with the instructions message.
        """
        self.console.print(
            Panel(self.get_settings_instructions(),
                title="[bold red]Settings[/] - [bold white]Instructions[/]",
                title_align="center",
                border_style="cyan",
            )
        )

    def print_database_instructions(self) -> Panel:
        """
        Print the commands for the database portion of the app.
        
        Return: The rendered panel with the instructions message.
        """
        self.console.print(
            Panel(self.get_database_instructions(),
                title="[bold red]Database Manager[/] - [bold white]Instructions[/]",
                title_align="center",
                border_style="cyan",
            )
        )
