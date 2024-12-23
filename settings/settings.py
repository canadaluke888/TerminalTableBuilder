from message_panel.message_panel import MessagePanel
from rich.table import Table
import json
from autocomplete.autocomplete import Autocomplete
from rich.console import Console


class Settings:
    
    def __init__(self, console: Console):
        """
        Initialize database.

        :param console: The main console for the app that will allow us to print to the screen.
        """
        
        self.console = console
        self.autocomplete = Autocomplete(self.console)
        self.settings_file = "settings/settings.json"
        self.message_panel = MessagePanel(self.console)
        self.settings = self.load_settings()
        
    def launch_settings(self):

        if self.get_hide_instructions() == "off":
            self.message_panel.print_settings_instructions()
        
        while True:
            setting = self.console.input("[bold red]Settings[/] - [bold yellow]Enter a setting[/]: ").lower().strip()
            
            if setting == "autoprint_table":
                value = self.console.input("[bold yellow]Turn Autoprint on or off[/]: ").lower().strip()
                self.set_autoprint_table(value)
                self.save_settings()

            elif setting == "hide_instructions":
                value = self.console.input("[bold yellow]Turn Hide Instructions on or off[/]: ").lower().strip()
                self.set_hide_instructions(value)
                self.save_settings()

            elif setting == "auto_update":
                value = self.console.input("[bold yellow]Turn Auto Update on or off[/]: ").lower().strip()
                self.set_auto_update(value)
                self.save_settings()

            elif setting == "print settings":
                self.print_settings()
                
            elif setting == "exit":
                break
                
            else:
                self.message_panel.create_error_message("Invalid Input.")
                self.autocomplete.suggest_command(setting, self.autocomplete.settings_commands)
                
    def load_settings(self):
        try:
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Default settings if file is missing or corrupted
            return {"autoprint_table": False,
                    "hide_instructions": False,
                    "auto_update": False}
        
    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)
        
    def print_settings(self):
        table = Table(title="Settings", border_style="yellow", show_lines=True)
        table.add_column("Setting", style="cyan")
        table.add_column("Description", style="green")
        table.add_column("Value", style="magenta")
        
        # Dynamically add rows from settings dictionary
        for setting, value in self.settings.items():
            description = self.get_setting_description(setting)
            table.add_row(setting, description, "on" if value else "off")
        
        self.console.print(table)
        
    def get_setting_description(self, setting: str) -> str:
        descriptions = {
            "autoprint_table": "Automatically prints the table after a change has been made.",
            "hide_instructions": "Hide the instructions message when using the app.",
            "auto_update": "Automatically update the database table when a change is made."
        }
        return descriptions.get(setting, "No description available.")
    
    def get_autoprint_table(self) -> str:
        value = self.settings.get("autoprint_table", False)
        return "on" if value else "off"
    
    def set_autoprint_table(self, value: str):
        value = value.lower().strip()
        if value == "on":
            self.settings["autoprint_table"] = True
            self.message_panel.create_information_message("autoprint_table [bold green]on[/]")
        elif value == "off":
            self.settings["autoprint_table"] = False
            self.message_panel.create_information_message("autoprint_table [bold red]off[/]")
        else:
            self.message_panel.create_error_message("Enter 'on' or 'off'.")

    def get_hide_instructions(self):
        value = self.settings.get("hide_instructions", False)
        return "on" if value else "off"
    
    def set_hide_instructions(self, value: str):
        value = value.lower().strip()

        if value == "on":
            self.settings['hide_instructions'] = True
            self.message_panel.create_information_message("hide_instructions [bold green]on[/]")
        elif value == "off":
            self.settings['hide_instructions'] = False
            self.message_panel.create_information_message("hide_instructions [bold red]off[/]")
        else:
            self.message_panel.create_error_message("Enter 'on' or 'off'.")

    def set_auto_update(self, value: str):
        value = value.lower().strip()

        if value == "on":
            self.settings['auto_update'] = True
            self.message_panel.create_information_message("auto_update [bold green]on[/]")
        elif value == "off":
            self.settings['auto_update'] = False
            self.message_panel.create_information_message("auto_update [bold red]off[/]")
        else:
            self.message_panel.create_error_message("Enter 'on' or 'off'.")

    def get_auto_update(self):
        value = self.settings.get("auto_update", False)
        return "on" if value else "off"