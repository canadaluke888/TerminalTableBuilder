import csv
import os

class CSVHandler:
    def __init__(self, table_builder):
        self.table_builder = table_builder

    def save_csv(self) -> None:
        """
        Save the current table data to a CSV file.
        """
        use_table_name = self.table_builder.input_handler.get_user_input(
            "[bold yellow]Use table name as save file name? (y/n)[/]: ").lower().strip()

        if use_table_name == "y":
            file_name = f"{self.table_builder.name}.csv"
        elif use_table_name == "n":
            file_name = self.table_builder.input_handler.get_user_input(
                "[bold yellow]Enter the name of the file (without extension)[/]: ") + ".csv"
        else:
            self.table_builder.system_message.create_error_message("Invalid input.")
            return

        # Write table data to the CSV file
        try:
            with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)

                # Write header row (columns)
                if self.table_builder.table_data["columns"]:
                    writer.writerow(self.table_builder.table_data["columns"])

                # Write data rows
                for row in self.table_builder.table_data["rows"]:
                    writer.writerow([row.get(column, "") for column in self.table_builder.table_data["columns"]])

            self.table_builder.table_saved = True
            self.table_builder.system_message.create_information_message(
                f"Table data successfully saved to '[bold red]{file_name}[/]'."
            )
        except Exception as e:
            self.table_builder.system_message.create_error_message(f"Failed to save file: {e}")

    def load_csv(self, path: str = None) -> None:
        """
        Load a CSV file and update the table data with all columns defaulting to strings.

        Args:
            path (str): Path to the CSV file. If not provided, prompts the user.
        """
        # Prompt for CSV path if not provided through CLI arg.
        csv_path = path or self.table_builder.input_handler.get_user_input("[bold yellow]Enter path to CSV file[/]: ").strip()

        if csv_path is None:
            return

        # Validate the file path
        if not os.path.isfile(csv_path):
            self.table_builder.system_message.create_error_message("Invalid path or file does not exist.")
            return

        try:
            with open(csv_path, 'r', encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file)
                rows = list(reader)  # Convert CSV reader to a list of rows

                # Ensure the CSV is not empty
                if not rows:
                    self.table_builder.system_message.create_error_message("CSV file is empty.")
                    return

                # Use the first row as column names, defaulting to string type
                self.table_builder.table_data["columns"] = [{"name": col, "type": "str"} for col in rows[0]]

                # Populate the rows with column-value dictionaries
                self.table_builder.table_data["rows"] = [
                    {col: value for col, value in zip([c["name"] for c in self.table_builder.table_data["columns"]], row)}
                    for row in rows[1:]
                ]

                self.table_builder.table_specs.infer_column_types() # Infer column types and apply
                self.table_builder.name = os.path.splitext(os.path.basename(csv_path))[0] # Change table name to file basename without extension
                self.table_builder.table_saved = False # Mark the table as unsaved
                self.table_builder.system_message.create_information_message("CSV file loaded successfully.")

        except UnicodeDecodeError:
            self.table_builder.system_message.create_error_message("Failed to decode file. Ensure it is UTF-8 encoded.")
        except Exception as e:
            self.table_builder.system_message.create_error_message(f"Failed to load CSV file: {e}")

    def load_batch_csv(self) -> None:
        """
        Load multiple CSV files from a specified directory into the database.
        """
        directory = self.table_builder.input_handler.get_user_input("[bold yellow]Enter the directory of CSV files[/]: ").strip()

        if directory is None:
            return

        # Ensure a database is connected
        if not self.table_builder.database_handler.ensure_connected_database():
            self.table_builder.system_message.create_error_message("No database is connected")
            return

        # Validate directory path
        if not os.path.exists(directory) or not os.path.isdir(directory):
            self.table_builder.system_message.create_error_message("Directory does not exist or is invalid.")
            return

        recursive_load = self.table_builder.input_handler.get_user_input("[bold yellow]Load CSV files from subdirectories? (y/n)[/]: ").strip().lower()
        csv_files = []

        # Collect CSV files
        try:
            if recursive_load == 'y':
                for root, _, files in os.walk(directory):
                    csv_files.extend([os.path.join(root, file) for file in files if file.endswith('.csv')])
            elif recursive_load == 'n':
                csv_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.csv')]
            else:
                self.table_builder.system_message.create_error_message("Invalid input! Please enter 'y' or 'n'.")
                return
        except Exception as e:
            self.table_builder.system_message.create_error_message(f"Error accessing directory: {e}")
            return

        if not csv_files:
            self.table_builder.system_message.create_error_message("No CSV files found in the specified directory.")
            return

        self.table_builder.system_message.create_information_message(f"Found [bold cyan]{len(csv_files)}[/] CSV files.")


        existing_tables = self.table_builder.database_handler.get_tables()  # Get list of existing tables

        for file in csv_files:
            try:
                self.load_csv(path=file)

                base_name = os.path.splitext(os.path.basename(file))[0]  # Use filename as default table name
                if base_name in existing_tables:
                    # Prompt user to rename or use default
                    user_choice = self.table_builder.input_handler.get_user_input(
                        f"[bold yellow]Table '{base_name}' already exists. Enter a new name or press Enter to use default.[/]: "
                    ).strip()

                    if not user_choice:
                        base_name = f"Table {self.table_builder.table_specs.next_table_number()}"

                self.table_builder.name = base_name
                self.table_builder.database_handler.save_to_database()

                self.table_builder.system_message.create_information_message(f"Successfully loaded table '[bold cyan]{self.table_builder.name}[/]' from file '[bold red]{file}[/]'.")
            except Exception as e:
                self.table_builder.system_message.create_error_message(f"Error processing '[bold blue]{file}[/]': {e}")

        self.table_builder.table_saved = True
        self.table_builder.system_message.create_information_message("Batch CSV loading complete!")