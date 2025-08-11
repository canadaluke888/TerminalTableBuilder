from message_panel.system_message import SystemMessage
from message_panel.instruction_message import InstructionMessage
from rich.table import Table
import json
from autocomplete.autocomplete import Autocomplete
from rich.console import Console
from rich.console import Group
from rich.panel import Panel
from .styles.styles import StylesSetting
from app_utils.app_utils import get_resource_path

class Settings:
    
    def __init__(self, console: Console):
        """
        Initialize database.

        :param console: The main console for the app that will allow us to print to the screen.
        """
        
        self.console = console
        self.autocomplete = Autocomplete(self.console)
        self.settings_file = get_resource_path(__file__, "settings.json")
        self.system_message = SystemMessage(self.console)
        self.instruction_message = InstructionMessage(self.console)
        self.settings = self.load_settings_from_file()
        self.styles_settings = StylesSetting(self)

        # Available settings and their descriptions
        self.settings_definitions = {
            "autoprint_table": "Automatically prints the table after a change has been made.",
            "hide_instructions": "Hide the instructions message when using the app.",
            "auto_update": "Automatically update the database table when a change is made.",
            "infer_data_types": "Enable automatic type inference when loading data."
        }
        
    def launch_settings(self) -> None:
        """
        Launch the Settings interface.
        """

        if self.get_setting("hide_instructions") == "off":
            self.print_settings_instructions()
        
        while True:
            setting = self.console.input("[bold red]Settings[/] - [bold yellow]Enter a setting[/]: ").lower().strip()
            
            if setting in self.settings_definitions:
                value = self.console.input(f"[bold yellow]Turn {setting} [bold green]on[/] or [bold red]off[/][/]: ").lower().strip()
                self.set_setting(setting, value)
                self.save_settings()
            elif setting == "styles":
                self.styles_settings.launch_styles()
            elif setting == "print current settings":
                self.print_current_settings()
            elif setting == "default settings":
                self.return_settings_to_default()
            elif setting == "help":
                self.print_settings_instructions()
            elif setting == "exit":
                break
            else:
                self.system_message.create_error_message("Invalid Input.")
                self.autocomplete.suggest_command(setting, self.autocomplete.settings_commands)
                
    def load_settings_from_file(self) -> dict:
        """
        Loads settings data from settings file.

        Returns:
            dict: Dictionary of all settings and their values. Factory settings are set if file not found or corrupt.
        """
        try:
            with open(self.settings_file, 'r') as f:
                settings =  json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):

            self.system_message.create_error_message("Unable to load settings. Loading defaults.")

            # Default settings if file is missing or corrupted
            settings =  {
                "autoprint_table": False,
                "hide_instructions": False,
                "auto_update": False,
                "infer_data_types": True
                }
        return settings        

    def save_settings(self) -> None:
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def print_settings_instructions(self) -> None:
        """
        Print the commands for the settings.
        
        Return: The rendered panel with the settings instructions as well as the current settings.
        """
        self.console.print(
            Panel(Group(self.instruction_message.get_settings_instructions(), self.get_current_settings()),
                title="[bold red]Settings[/] - [bold white]Instructions[/]",
                title_align="center",
                border_style="cyan",
            )
        )
        
    def get_current_settings(self) -> Table:
        table = Table(title="[bold blue]Current Settings[/]", border_style="yellow", show_lines=True)
        table.add_column("Setting", style="cyan")
        table.add_column("Description", style="green")
        table.add_column("Value", style="magenta")
        
        # Dynamically add rows from settings dictionary
        for setting, description in self.settings_definitions.items():
            value = "on" if self.settings.get(setting, False) else "off"
            table.add_row(setting, description, value)
        
        return table
    
    def print_current_settings(self) -> None:
        self.console.print(self.get_current_settings())

    def get_setting(self, setting: str) -> str:
        """
        Retrieve the value of a given setting.
        
        Args:
            setting (str): The setting key.
        
        Returns:
            str: "on" if True, "off" otherwise.
        """
        return "on" if self.settings.get(setting, False) else "off"

    def set_setting(self, setting: str, value: str) -> None:
        """
        Update a setting value dynamically.

        Args:
            setting (str): The setting key.
            value (str): "on" to enable, "off" to disable.
        """
        value = value.lower().strip()
        if setting not in self.settings_definitions:
            self.system_message.create_error_message(f"Invalid setting: {setting}")
            return
        
        if value == "on":
            self.settings[setting] = True
            self.system_message.create_information_message(f"{setting} [bold green]on[/]")
        elif value == "off":
            self.settings[setting] = False
            self.system_message.create_information_message(f"{setting} [bold red]off[/]")
        else:
            self.system_message.create_error_message("Enter 'on' or 'off'.")

    def return_settings_to_default(self):

        confirm = self.console.input("[bold red]Are you sure you want to reset settings to defaults? (y/n)[/]: ")


        if confirm == "y":
            self.settings = {
                "autoprint_table": False,
                "hide_instructions": False,
                "auto_update": False,
                "infer_data_types": True,
                }
            self.save_settings()
            self.system_message.create_information_message("Settings reset to defaults.")
        elif confirm == "n":
            return
        else:
            self.system_message.create_error_message("Invalid input. Please enter 'y' or 'n'.")
