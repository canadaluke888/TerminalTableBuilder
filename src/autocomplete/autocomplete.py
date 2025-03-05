from difflib import get_close_matches
import json
from message_panel.system_message import SystemMessage
from functools import cache
from rich.console import Console

class Autocomplete:
    
    def __init__(self, console: Console):
        """
        Initialize console and command lists.

        :param console: Main console.
        """
        
        self.console = console
        
        self.cutoff = 0.6
        
        self.system_message = SystemMessage(self.console)
        
        self.command_list_file = "autocomplete/command_list.json"
        
        self.all_commands = self.load_command_list()
        
        self.main_menu_commands = self.get_main_menu_commands()
        
        self.settings_commands = self.get_settings_commands()
        
        self.table_builder_commands = self.get_table_builder_commands()
        
        self.database_commands = self.get_database_commands()

        self.style_commands = self.get_style_commands()
        
    @cache
    def load_command_list(self) -> dict:
        """
        Load the complete list of commands from file.

        Returns:
            dict: The dictionary containing the lists of commands for each section of the app.
        """
        with open(self.command_list_file, 'r') as f:
            return json.load(f)
        
    @cache
    def get_main_menu_commands(self) -> list:
        """
        Extracts the main menu commands from the complete list of commands.

        Returns:
            list: The complete list of main menu commands.
        """
        return self.all_commands.get("main_menu")
    
    @cache
    def get_settings_commands(self) -> list:
        """
        Extracts the settings commands from teh complete list of commands.

        Returns:
            list: The complete list of settings commands.
        """
        return self.all_commands.get("settings")
    
    @cache
    def get_table_builder_commands(self) -> list:
        """
        Extracts the table builder commands from the complete list of commands.

        Returns:
            list: The complete list of table builder commands.
        """
        return self.all_commands.get("table_builder")
    
    @cache
    def get_database_commands(self) -> list:
        """
        Extracts the database commands from the complete list of commands.

        Returns:
            list: The complete list of database commands.
        """
        return self.all_commands.get("database")
    
    @cache
    def get_style_commands(self) -> list:
        """
        Extracts the style command from the complete list of commands.

        Returns:
            list: The complete list of style commands.
        """
        return self.all_commands.get("styles")
    
    def suggest_command(self, user_input: str, commands: list) -> SystemMessage:
        """
        Suggest the closest commands to the user's input.

        :param user_input: The command input by the user.
        :param commands: The list of commands for the specified app section.
        :return MessagePanel: The formatted message panel with the suggested command.
        """
        matches = get_close_matches(user_input, commands, n=1, cutoff=self.cutoff)
        if matches:
            formatted_matches = ", ".join([f"'{match}'" for match in matches])
            self.system_message.create_information_message(
                f"Did you mean: {formatted_matches}?"
            )
        else:
            return