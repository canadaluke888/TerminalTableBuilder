from rich.table import Table
from rich.console import Group
from rich.panel import Panel
import json


class StylesSetting:

    def __init__(self, settings):
        self.settings = settings
        self.colors_file = "settings/styles/colors.json"
        self.user_styles_file = "settings/styles/user_styles.json"
        self.colors = self.load_colors_from_file()
        self.user_styles = self.load_user_styles_from_file()


    def load_user_styles_from_file(self) -> dict:
        
        try:
            with open(self.user_styles_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.settings.system_message.create_error_message("Could not load user styles. Loading defaults.")
            return {
                "table": {
                        "border_style": "yellow",
                        "row_style": "magenta",
                        "column_style": "cyan"
                    }
                }   
    def save_user_styles(self) -> None:
        """
        Save the current style settings to file.
        """
        with open(self.user_styles_file, 'w') as f:
            json.dump(self.user_styles, f, indent=4)

    def get_table_border_style(self) -> str:
        """
        Returns the current table border style set by the user.

        Returns:
            str: Set color.
        """
        return self.user_styles["table"].get("table_border_style")
    
    def get_table_title_style(self) -> str:
        return self.user_styles["table"].get("table_title_style")

    def get_table_row_style(self) -> str:
        """
        Returns the current table row style set by the user.

        Returns:
            str: Set color.
        """
        return self.user_styles["table"].get("row_style")


    def set_table_border_style(self, color: str) -> None:
        self.user_styles["table"]["table_border_style"] = color
        self.save_user_styles()

    def set_table_title_style(self, color: str) -> None:
        self.user_styles["table"]["table_title_style"] = color
        self.save_user_styles()

    def set_table_row_style(self, color: str) -> None:
        self.user_styles["table"]["row_style"] = color
        self.save_user_styles()
        
    def choose_color(self) -> str:
        """
        Display available colors and allow the user to select one.

        Returns:
            str: The selected color name.
        """
        if not self.colors:
            self.settings.console.print("[bold red]No colors available to choose from.[/]")
            return None

        table = Table(title="Available Colors", show_lines=True, border_style="yellow")
        table.add_column("#", style="cyan", justify="center")
        table.add_column("Color Name", style="magenta", justify="left")
        
        # Display colors with corresponding index
        for i, color in enumerate(self.colors, start=1):
            table.add_row(str(i), f"[{color}]{color}[/]")

        self.settings.console.print(table)

        while True:
            try:
                selected_index = int(self.settings.console.input("[bold yellow]Enter the number of the color you want to select[/]: ").strip()) - 1
                if 0 <= selected_index < len(self.colors):
                    return self.colors[selected_index]
                else:
                    self.settings.console.print("[bold red]Invalid selection. Please enter a valid number.[/]")
            except ValueError:
                self.settings.console.print("[bold red]Invalid input. Please enter a number.[/]")

    def load_colors_from_file(self) -> list:
        """
        Loads the list of colors that can be set.

        Returns:
            list: The complete list of color names.
        """
        try:
            with open(self.colors_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
             self.system_message.create_error_message(f"Unable to load color file: {e}")

    def get_current_user_styles(self) -> Table:
        """
        Returns the current user styles in a rendered table.

        Returns:
            Table: The style settings and their current values.
        """
        # Table Styles Table
        table = Table(title="[bold red]Table Styles[/]", border_style="yellow", show_lines=True)
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="magenta")

        for setting, value in self.user_styles["table"].items():
            table.add_row(setting, str(value))

        return table

    def print_styles_instructions(self) -> None:
        """
        Prints the current styles table to the sc
        """

        panel = Panel(Group(self.settings.instruction_message.get_styles_instructions(), self.get_current_user_styles()),
                      title="[bold red]Styles[/] - [bold white]Instructions[/]",
                      title_align="center",
                      border_style="white")

        self.settings.console.print(panel)

    def print_current_user_styles(self) -> None:
        self.settings.console.print(self.get_current_user_styles())

    def launch_styles(self):

        if self.settings.get_setting("hide_instructions") == "off":
            self.print_styles_instructions()

        while True:

            styles_command = self.settings.console.input("[bold red]Styles[/] - [bold yellow]Enter a command[/]: ").lower().strip()

            if styles_command == "set border style":

                color = self.choose_color()

                self.set_table_border_style(color)

                self.settings.system_message.create_information_message(f"Table Border style set to [{color}]{color}[/]")

            elif styles_command == "set table title style":

                color = self.choose_color()

                self.set_table_title_style(color)

                self.settings.system_message.create_information_message(f"Table title style set to [{color}]{color}[/]")


            elif styles_command == "set row style":

                color = self.choose_color()

                self.set_table_row_style(color)

                self.settings.system_message.create_information_message(f"Row style set to [{color}]{color}[/]")

            elif styles_command == "print current styles":
                self.print_current_user_styles()

            elif styles_command == "help":
                self.print_styles_instructions()

            elif styles_command == "exit":
                break

            else:
                self.settings.system_message.create_error_message("Invalid input.")
                self.settings.autocomplete.suggest_command(styles_command, self.settings.autocomplete.style_commands)