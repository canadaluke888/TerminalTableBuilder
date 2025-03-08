from pyexcel_ods3 import get_data, save_data
import os

class ODSHandler:
    def __init__(self, table_builder):
        self.table_builder = table_builder

    def load_ods(self, path: str | os.PathLike = None) -> None:
        """
        Load table data from an .ods file using pyexcel-ods3.
        """
        file_name = path or self.table_builder.input_handler.get_user_input("[bold yellow]Enter path to the ODS file[/]: ").strip()

        if file_name is None:
            return

        if not os.path.exists(file_name):
            self.table_builder.system_message.create_error_message("File not found.")
            return

        try:
            data = get_data(file_name)
            sheet_name = list(data.keys())[0]  # Ensure we get the first sheet correctly
            sheet_data = data[sheet_name]

            if not sheet_data or not isinstance(sheet_data, list):
                self.table_builder.system_message.create_error_message("The ODS file is empty or has an invalid format.")
                return

            self.table_builder.table_data["columns"] = [{"name": col, "type": "str"} for col in sheet_data[0]]
            self.table_builder.table_data["rows"] = [{col: row[i] if i < len(row) else "" for i, col in enumerate(sheet_data[0])} for row in sheet_data[1:]]
            self.table_builder.name = os.path.splitext(os.path.basename(file_name))[0]
            if self.table_builder.settings.get_setting("infer_data_types") == "on":
                self.table_builder.table_specs.infer_column_types()
            self.table_builder.system_message.create_information_message("ODS file loaded successfully.")
        except Exception as e:
            self.table_builder.system_message.create_error_message(f"Failed to load ODS file: {e}")

    def save_ods(self) -> None:
        """
        Save the current table data to an .ods file using pyexcel-ods3.
        """
        if not self.table_builder.table_data["columns"] or not self.table_builder.table_data["rows"]:
            self.table_builder.system_message.create_error_message("No table data to export to ODS.")
            return
        
        use_table_name = self.table_builder.input_handler.get_user_input("[bold yellow]Use table name as save file name? (y/n): ")
        
        if use_table_name == "y":
            file_name = f"{self.table_builder.name}.ods"
        elif use_table_name == "n":
            file_name = self.table_builder.input_handler.get_user_input("[bold yellow]Enter the name of the ODS file (without extension)[/]: ").strip() + ".ods"
        elif use_table_name is None:
            return
        else:
            self.table_builder.system_message.create_error_message("Invalid input.")
            return

        try:
            column_headers = [col["name"] for col in self.table_builder.table_data["columns"]]
            data = [[col for col in column_headers]]
            data.extend([[row.get(col, "") for col in column_headers] for row in self.table_builder.table_data["rows"]])

            save_data(file_name, {"Sheet1": data})
            self.table_builder.system_message.create_information_message(f"Table data successfully saved to '[bold cyan]{file_name}[/]'.")
        except Exception as e:
            self.table_builder.system_message.create_error_message(f"Failed to save table as ODS file: {e}")

    