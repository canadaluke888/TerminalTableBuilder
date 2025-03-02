import json

class JSONHandler:

    def __init__(self, table_builder):
        self.table_builder = table_builder


    def save_json(self):
        """Save the table data to a JSON file."""
        use_table_name = self.table_builder.input_handler.get_user_input(
            "[bold yellow]Use table name as save file name? (y/n)[/]: ").lower().strip()

        if use_table_name == "y":
            file_name = f"{self.table_builder.name}.json"
        elif use_table_name == "n":
            file_name = self.table_builder.input_handler.get_user_input(
                "[bold yellow]Enter the name of the file (without extension)[/]: ") + ".json"
            if file_name is None:
                return
        elif file_name is None:
            return
        else:
            self.table_builder.system_message.create_error_message("Invalid input.")
            return
        
        with open(file_name, 'w') as f:
            json.dump(self.table_builder.table_data, f, indent=4)

            self.table_builder.table_saved = True
            self.table_builder.system_message.create_information_message(
                f"Table data successfully saved to '[bold red]{file_name}[/]'."
            )