from rich.console import Console
from message_panel.system_message import SystemMessage
from message_panel.instruction_message import InstructionMessage
from table_builder.builder import TableBuilder
from settings.settings import Settings
from autocomplete.autocomplete import Autocomplete
from database.database import Database

console = Console()
system_message = SystemMessage(console)
instruction_message = InstructionMessage(console)
autocomplete = Autocomplete(console)
settings = Settings(console)
database = Database(console, settings)


def main():
    """
    Start main application loop.
    """
    
    instruction_message.print_welcome_message()
    
    while True:
        
        main_menu_command = console.input("[bold red]Main Menu[/] - [bold yellow]Enter a command[/]: ").lower().strip()
        
        if main_menu_command == "table builder":
            table_builder = TableBuilder(console, settings, database)
            table_builder.launch_builder()
            
        elif main_menu_command == "database":
            database.launch_database()
        
        elif main_menu_command == "settings":
            settings.launch_settings()
            
        elif main_menu_command == "help":
            instruction_message.print_main_menu_instructions()
            
        elif main_menu_command == "exit":
            break
        else:
            system_message.create_error_message("Invalid input.")
            autocomplete.suggest_command(main_menu_command, autocomplete.main_menu_commands)
        
if __name__ == "__main__":
    main()