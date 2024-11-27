from rich.console import Console
from message_panel.message_panel import MessagePanel
from table_builder.table_builder import TableBuilder
from settings.settings import Settings

console = Console()
message_panel = MessagePanel(console)
settings = Settings(console)


def main():
    
    message_panel.print_welcome_message()
    
    while True:
        
        main_menu_command = console.input("[bold red]Main Menu[/] - [bold yellow]Enter a command[/]: ").lower().strip()
        
        if main_menu_command == "table_builder":
            table_builder = TableBuilder(console, settings)
            table_builder.launch_builder()
            
        elif main_menu_command == "settings":
            settings.launch_settings()
            
        elif main_menu_command == "exit":
            break
        
if __name__ == "__main__":
    main()