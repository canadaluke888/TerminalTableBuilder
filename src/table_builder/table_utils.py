import re

class InputHandler:

    def __init__(self, table_builder):
        self.table_builder = table_builder

    def get_user_input(self, prompt: str) -> str:
        """
        Get user input and allow cancellation.

        Args:
            prompt (str): The prompt to display to the user.

        Returns:
            str: The input from the user. If '/cancel', return None.
        """
        while True:
            user_input = self.table_builder.console.input(prompt).strip()
            if user_input == "/cancel":
                return None
            return user_input

    @staticmethod
    def infer_data_type( value: str) -> str:
        """
        Infer a column header's type based on its content.

        Args:
            type (str): The column to be inferred.

        Returns:
            str: The inferred type.
        """
        value = value.strip()

        # Check for boolean values
        if value.lower() in {"true", "false"}:
            return "bool"
        
        # Check for integer values
        if re.fullmatch(r"-?\d+", value):
            return "int"
        
        # Check for float values
        if re.fullmatch(r"-?\d+\.\d+", value):
            return "float"
        
        # Default to string if no other match
        return "str"
        
        
class TableSpecs:

    def __init__(self, table_builder):
        self.table_builder = table_builder

    def get_num_columns(self) -> int:
        """
        Returns:
            int: The total amount of columns in the table.
        """
        return len(self.table_builder.table_data["columns"])

    def get_num_rows(self) -> int:
        """
        Returns:
            int: The total amount of rows in the table.
        """
        return len(self.table_builder.table_data["rows"])
    
    def show_current_table(self) -> None:
        """
        Prints the current table in a message panel.
        """
        self.table_builder.system_message.create_information_message(f"Current Table: [bold cyan]{self.table_builder.name}[/]")

    def next_table_number(self) -> int:
        """
        Returns: 
            int: he next available table number based on the existing tables in the current database.
        """
        existing_tables = self.table_builder.database_handler.get_tables()
        return len(existing_tables) + 1
    
    def infer_column_types(self) -> None:
        """
        Infers data types for each column in the table based on the first non-empty row.

        Updates:
            self.table_builder.table_data["columns"]: Assigns the inferred type to each column.
        """
        if not self.table_builder.table_data["rows"]:
            self.table_builder.system_message.create_information_message("No data to infer column types from.")
            return

        # Get the first non-empty row
        first_data_row = next((row for row in self.table_builder.table_data["rows"] if any(row.values())), None)

        if not first_data_row:
            self.table_builder.system_message.create_error_message("Could not infer types, no valid data found.")
            return

        # Infer types using the first non-empty row
        for column in self.table_builder.table_data["columns"]:
            column_name = column["name"]
            value = first_data_row.get(column_name, "")

            if value:
                column["type"] = self.table_builder.input_handler.infer_data_type(value)
