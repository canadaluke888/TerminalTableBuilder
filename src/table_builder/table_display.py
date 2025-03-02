from rich.table import Table
from rich.panel import Panel
from settings.styles.styles import StylesSetting

class TableDisplay:

    def __init__(self, table_builder):
        self.table_builder = table_builder
        self.user_styles = StylesSetting(self.table_builder.settings)
        self.table_border_style = self.user_styles.get_table_border_style()
        self.table_column_style = self.user_styles.get_table_column_style()
        self.table_row_style = self.user_styles.get_table_row_style()
        


    def build_table(self) -> Table:
        """
        Takes the current table data and builds the table with it.

        Returns:
            Table: The rendered table with all of the data.
        """
        if not self.table_builder.table_data["columns"]:
            self.table_builder.system_message.create_error_message("No columns defined. Add columns before building the table.")
            return Table(border_style="yellow", show_lines=True)

        # Create a Rich Table instance
        table = Table(title=self.table_builder.name, border_style=self.table_border_style, show_lines=True)

        # Add columns with type information
        for column in self.table_builder.table_data["columns"]:
            column_name = column["name"]
            column_type = column["type"]
            table.add_column(f"{column_name} ([bold red]{column_type}[/])", style=self.table_column_style)

        # Add rows
        for row in self.table_builder.table_data["rows"]:
            row_values = [str(row.get(column["name"], "")) for column in self.table_builder.table_data["columns"]]
            table.add_row(*row_values, style=self.table_row_style)

        return table
    
    def print_table(self) -> None:
        """
        Prints the built table to the screen.
        """
        table = self.table_builder.table_display.build_table()
        self.table_builder.console.print(table)

    def print_table_data(self) -> Panel:
        """
        Prints the table data to the screen.
        """
        self.table_builder.console.print(Panel(str(self.table_builder.table_data), title="[bold red]Table Data[/]", title_align="center", border_style="cyan"))

    def list_tables(self) -> None:
        """
        List all tables in the connected database.
        """
        if not self.table_builder.database_handler.ensure_connected_database():
            self.table_builder.system_message.create_error_message("No database connected.")
            return

        try:
            self.table_builder.database.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in self.table_builder.database.cursor.fetchall()]

            if tables:
                self.table_builder.console.print("[bold green]Available Tables:[/]")
                for idx, table in enumerate(tables, start=1):
                    self.table_builder.console.print(f"{idx}. {table}")
            else:
                self.table_builder.system_message.create_error_message("No tables found in the database.")
        except Exception as e:
            self.table_builder.system_message.create_error_message(f"Failed to list tables: {e}")

    def show_current_table(self):
        self.table_builder.system_message.create_information_message(f"Current Table: [bold cyan]{self.table_builder.name}[/]")