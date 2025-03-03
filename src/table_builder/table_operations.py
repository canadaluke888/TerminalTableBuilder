class TableOperations:

    def __init__(self, table_builder):
        self.table_builder = table_builder

    def name_table(self) -> str:
        self.table_builder.table_saved = False
        return self.table_builder.input_handler.get_user_input("[bold yellow]Enter a name for the new table[/]: ")

    def add_column(self) -> None:
        column_name = self.table_builder.input_handler.get_user_input("[bold yellow]Enter column name[/]: ")
        if column_name is None:
            return

        if column_name in [col["name"] for col in self.table_builder.table_data["columns"]]:
            self.table_builder.system_message.create_error_message("Column already exists.")
            return

        types = ["int", "float", "str", "bool"]
        self.table_builder.console.print("[bold green]Available Types:[/]")
        for idx, t in enumerate(types, start=1):
            self.table_builder.console.print(f"{idx}. {t}")

        while True:
            type_number = self.table_builder.input_handler.get_user_input("[bold yellow]Enter the number of the type for this column[/]: ")
            if type_number is None:
                return
            try:
                type_number = int(type_number) - 1
                if not (0 <= type_number < len(types)):
                    self.table_builder.system_message.create_error_message("Invalid type number. Try again.")
                    continue
                selected_type = types[type_number]
                break
            except ValueError:
                self.table_builder.system_message.create_error_message("Invalid input. Please enter a number.")
                continue

        self.table_builder.table_data["columns"].append({"name": column_name, "type": selected_type})
        for row in self.table_builder.table_data["rows"]:
            row[column_name] = ""
        self.table_builder.table_saved = False
        self.table_builder.system_message.create_information_message(f"Column '[bold cyan]{column_name}[/]' added with type '[bold red]{selected_type}[/]'.")

    def change_column_type(self) -> None:
        """
        Change the data type of a specific column in the table.
        """
        if not self.table_builder.table_data["columns"]:
            self.table_builder.system_message.create_error_message("No columns defined. Add columns before changing types.")
            return

        # Display available columns for selection
        self.table_builder.console.print("[bold green]Available Columns[/]:")
        for idx, column in enumerate(self.table_builder.table_data["columns"], start=1):
            self.table_builder.console.print(f"{idx}. {column['name']} (Current Type: {column['type']})")

        try:
            column_number = int(self.table_builder.input_handler.get_user_input("[bold yellow]Enter the number of the column to change type[/]: ")) - 1
            if not (0 <= column_number < len(self.table_builder.table_data["columns"])):
                self.table_builder.system_message.create_error_message("Invalid column number.")
                return
            selected_column = self.table_builder.table_data["columns"][column_number]
        except ValueError:
            self.table_builder.system_message.create_error_message("Invalid input. Please enter a number.")
            return

        # Display available types for selection
        types = ["int", "float", "str", "bool"]
        self.table_builder.console.print("[bold green]Available Types[/]:")
        for idx, t in enumerate(types, start=1):
            self.table_builder.console.print(f"{idx}. {t}")

        try:
            type_number = int(self.table_builder.input_handler.get_user_input("[bold yellow]Enter the number of the new type[/]: ")) - 1
            if not (0 <= type_number < len(types)):
                self.table_builder.system_message.create_error_message("Invalid type number.")
                return
            new_type = types[type_number]
        except ValueError:
            self.table_builder.system_message.create_error_message("Invalid input. Please enter a number.")
            return

        # Confirm the change
        confirm = self.table_builder.input_handler.get_user_input(
            f"[bold red]Are you sure you want to change column '{selected_column['name']}' "
            f"from '{selected_column['type']}' to '{new_type}'? (y/n)[/]: "
        ).strip().lower()

        if confirm == "y":
            # Apply the type change
            selected_column["type"] = new_type
            self.table_builder.system_message.create_information_message(
                f"Column '[bold cyan]{selected_column['name']}[/]' type changed to '[bold red]{new_type}[/]'."
            )
            self.table_builder.table_saved = False
        else:
            self.table_builder.system_message.create_information_message("[bold yellow]Column type change cancelled.[/]")

    def edit_column_name(self) -> None:
        """
        Edits the name of an existing column in the table.
        """
        if not self.table_builder.table_data["columns"]:
            self.table_builder.system_message.create_error_message("No columns defined. Add columns before renaming.")
            return

        # Display available columns for selection
        self.table_builder.console.print("[bold green]Available Columns[/]:")
        for idx, column in enumerate(self.table_builder.table_data["columns"], start=1):
            self.table_builder.console.print(f"{idx}. {column['name']} (Type: {column['type']})")

        try:
            column_number = int(self.table_builder.input_handler.get_user_input("[bold yellow]Enter the number of the column to rename[/]: ")) - 1
            if not (0 <= column_number < len(self.table_builder.table_data["columns"])):
                self.table_builder.system_message.create_error_message("Invalid column number.")
                return
            selected_column = self.table_builder.table_data["columns"][column_number]
        except ValueError:
            self.table_builder.system_message.create_error_message("Invalid input. Please enter a number.")
            return

        # Prompt for the new column name
        new_name = self.table_builder.input_handler.get_user_input(f"[bold yellow]Enter the new name for column '[bold cyan]{selected_column['name']}[/]': [/]").strip()

        # Validate new name (e.g., avoid duplicates)
        if any(column["name"] == new_name for column in self.table_builder.table_data["columns"]):
            self.table_builder.system_message.create_error_message("A column with this name already exists. Please choose a different name.")
            return

        # Apply the name change
        old_name = selected_column["name"]
        selected_column["name"] = new_name

        # Update all row data to reflect the name change
        for row in self.table_builder.table_data["rows"]:
            row[new_name] = row.pop(old_name, "")

        self.table_builder.table_saved = False
        self.table_builder.system_message.create_information_message(f"Column '[bold cyan]{old_name}[/]' renamed to '[bold green]{new_name}[/]' successfully.")

    def add_row(self) -> None:
        """
        Adds a row to the table data with validation for column data types.
        """
        if not self.table_builder.table_data["columns"]:
            self.table_builder.system_message.create_error_message("No columns defined. Add columns before adding rows.")
            return
        
        row_data = {}
        for column in self.table_builder.table_data["columns"]:
            column_name = column["name"]
            data_type = column["type"]

            while True:
                cell_data = self.table_builder.input_handler.get_user_input(f"[bold yellow]Enter data for column '[bold cyan]{column_name}[/]' ([bold red]{data_type}[/]): ")
                if cell_data is None:
                    return
                if data_type == "int" and cell_data.isdigit():
                    row_data[column_name] = int(cell_data)
                    break
                elif data_type == "float":
                    try:
                        row_data[column_name] = float(cell_data)
                        break
                    except ValueError:
                        self.table_builder.system_message.create_error_message("Invalid data. Expected a float.")
                elif data_type == "bool" and cell_data.lower() in ["true", "false"]:
                    row_data[column_name] = cell_data.lower() == "true"
                    break
                elif data_type == "str":
                    row_data[column_name] = cell_data
                    break
                else:
                    self.table_builder.system_message.create_error_message("Invalid input. Please enter a valid value.")

        self.table_builder.table_data["rows"].append(row_data)
        self.table_builder.table_saved = False
        self.table_builder.system_message.create_information_message("Row added with validated data.")

    def edit_cell(self) -> None:
        """
        Edits the cell content using direct indexing.
        """
        if not self.table_builder.table_data["columns"] or not self.table_builder.table_data["rows"]:
            self.table_builder.system_message.create_error_message("No table data to edit. Add rows and columns first.")
            return

        # Display table cells with their indices
        self.table_builder.console.print("[bold green]Table Cells[/]:")
        for row_idx, row in enumerate(self.table_builder.table_data["rows"], start=1):
            row_display = [
                f"({row_idx},{col_idx + 1}) {row[col['name']]}" for col_idx, col in enumerate(self.table_builder.table_data["columns"])
            ]
            self.table_builder.console.print(f"Row {row_idx}: " + " | ".join(row_display))

        try:
            # Prompt for cell index
            cell_position = self.table_builder.input_handler.get_user_input("[bold yellow]Enter cell position as 'row,column' (e.g., 1,2)[/]: ").strip()
            if cell_position is None:
                return
            row_idx, col_idx = map(int, cell_position.split(","))
            row_idx -= 1  # Convert to 0-based index
            col_idx -= 1  # Convert to 0-based index

            if not (0 <= row_idx < len(self.table_builder.table_data["rows"]) and 0 <= col_idx < len(self.table_builder.table_data["columns"])):
                self.table_builder.system_message.create_error_message("Invalid cell position.")
                return

            # Fetch column and its type
            column = self.table_builder.table_data["columns"][col_idx]
            column_name = column["name"]
            column_type = column["type"]

            # Prompt for new value with type validation
            while True:
                new_data = self.table_builder.input_handler.get_user_input(f"[bold yellow]Enter new data for cell ([bold cyan]{row_idx + 1},{col_idx + 1}[/]) ([bold red]{column_name}[/]: [bold blue]{column_type})[/]): ").strip()
                if column_type == "int" and new_data.isdigit():
                    new_value = int(new_data)
                    break
                elif column_type == "float":
                    try:
                        new_value = float(new_data)
                        break
                    except ValueError:
                        self.table_builder.system_message.create_error_message("Invalid data. Expected a float.")
                elif column_type == "bool":
                    if new_data.lower() in ["true", "false"]:
                        new_value = new_data.lower() == "true"
                        break
                    else:
                        self.table_builder.system_message.create_error_message("Invalid data. Expected 'true' or 'false'.")
                elif column_type == "str":
                    new_value = new_data
                    break
                else:
                    self.table_builder.system_message.create_error_message(f"Unsupported data type: [bold cyan]{column_type}[/]")

            # Update the cell
            self.table_builder.table_data["rows"][row_idx][column_name] = new_value
            self.table_builder.table_saved = False
            self.table_builder.system_message.create_information_message("Cell updated successfully.")

        except ValueError:
            self.table_builder.system_message.create_error_message("Invalid input format. Use 'row,column'.")
        except Exception as e:
            self.table_builder.system_message.create_error_message(f"Failed to edit cell: {e}")

    def remove_column(self) -> None:
        """
        Removes a column based on the column name provided by the user.
        Aborts if the column name is not found or any error occurs.
        """
        column_name = self.table_builder.input_handler.get_user_input("[bold yellow]Enter column name to remove[/]: ").strip()

        # Check if the column exists
        column_names = [col["name"] for col in self.table_builder.table_data["columns"]]
        if column_name not in column_names:
            self.table_builder.system_message.create_error_message(f"Column '[bold cyan]{column_name}[/]' does not exist.")
            return

        try:
            # Remove the column from the table structure
            self.table_builder.table_data["columns"] = [
                col for col in self.table_builder.table_data["columns"] if col["name"] != column_name
            ]
            for row in self.table_builder.table_data["rows"]:
                row.pop(column_name, None)

            self.table_builder.table_saved = False
            self.table_builder.system_message.create_information_message(f"Column '[bold cyan]{column_name}[/]' removed successfully.")
            
        except Exception as e:
            self.table_builder.system_message.create_error_message(f"Failed to remove column: {e}")

    def remove_row(self) -> None:
        """
        Removes a row from the table based on the row index given.
        """
        row_number = int(self.table_builder.input_handler.get_user_input("[bold yellow]Enter row number to remove (1-based index)[/]: ")) - 1
        if 0 <= row_number < len(self.table_builder.table_data["rows"]):
            self.table_builder.table_data["rows"].pop(row_number)
            self.table_builder.table_saved = False
            self.table_builder.system_message.create_information_message("Row removed.")
        else:
            self.table_builder.system_message.create_error_message("Invalid row number.")

    def clear_table(self) -> None:
        """
        Clears the table data.
        """
        self.table_builder.table_data = {"columns": [], "rows": []}
        self.table_builder.system_message.create_information_message("Table cleared.")