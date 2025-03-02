import sqlite3

class DatabaseHandler:

    def __init__(self, table_builder):
        self.table_builder = table_builder


    def ensure_connected_database(self) -> bool:
        """
        Ensure there is a connected database before proceeding with table operations.
        """
        if not self.table_builder.database.is_connected():
            self.table_builder.system_message.create_error_message("No database connected.")
            return False
        return True
    
    def save_to_database(self) -> None:
        """
        Save the current table data to the connected database, with error handling to abort
        on any failure.
        """
        if not self.ensure_connected_database():
            return

        if not self.table_builder.table_data["columns"]:
            self.table_builder.system_message.create_error_message("No columns defined. Add columns before saving.")
            return

        try:
            quoted_table_name = f'"{self.table_builder.name}"'

            # Check if the table exists
            self.table_builder.database.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = [row[0] for row in self.table_builder.database.cursor.fetchall()]

            if self.table_builder.name in existing_tables:
                if self.table_builder.settings.get_auto_update() == "on":
                    # Auto-update: overwrite the existing table without prompting
                    self.table_builder.database.cursor.execute(f"DROP TABLE {quoted_table_name}")
                else:
                    # Prompt the user for action
                    action = self.table_builder.input_handler.get_user_input(
                        f"[bold yellow]Table '[bold cyan]{self.name}[/]' already exists. "
                        "Do you want to overwrite it or save with a new name? (overwrite/new)[/]: "
                    ).strip().lower()

                    if action == "overwrite":
                        self.table_builder.database.cursor.execute(f"DROP TABLE {quoted_table_name}")
                    elif action == "new":
                        new_name = self.table_builder.input_handler.get_user_input("[bold yellow]Enter a new name for the table[/]: ").strip()
                        if not new_name:
                            self.table_builder.system_message.create_error_message("Table name cannot be empty.")
                            return
                        self.table_builder.name = new_name
                        quoted_table_name = f'"{self.table_builder.name}"'
                    else:
                        self.table_builder.system_message.create_error_message("Invalid action. Please enter 'overwrite' or 'new'.")
                        return

            # Generate columns definition with data types
            columns_definition = []
            for column in self.table_builder.table_data["columns"]:
                column_name = f'"{column["name"]}"'
                column_type = column["type"].upper()
                if column_type == "STR":
                    column_type = "TEXT"
                elif column_type == "INT":
                    column_type = "INTEGER"
                elif column_type == "FLOAT":
                    column_type = "REAL"
                elif column_type == "BOOL":
                    column_type = "BOOLEAN"
                else:
                    self.table_builder.system_message.create_error_message(
                        f"Unsupported data type for column '[bold cyan]{column['name']}': {column['type']}[/]'"
                    )
                    return

                columns_definition.append(f"{column_name} {column_type}")
            columns_definition_str = ", ".join(columns_definition)

            # Create the table
            self.table_builder.database.cursor.execute(f"CREATE TABLE {quoted_table_name} ({columns_definition_str})")

            # Insert rows
            for row in self.table_builder.table_data["rows"]:
                column_names = ", ".join(f'"{col["name"]}"' for col in self.table_builder.table_data["columns"])
                placeholders = ", ".join("?" for _ in self.table_builder.table_data["columns"])
                values = [row.get(col["name"], None) for col in self.table_builder.table_data["columns"]]
                self.table_builder.database.cursor.execute(
                    f"INSERT INTO {quoted_table_name} ({column_names}) VALUES ({placeholders})", values
                )

            self.table_builder.database.connection.commit()
            self.table_builder.table_saved = True
            self.table_builder.system_message.create_information_message(
                f"Table '[bold cyan]{self.table_builder.name}[/]' saved to database '[bold red]{self.table_builder.database.get_current_database()}[/]'."
            )
        except Exception as e:
            self.table_builder.system_message.create_error_message(f"Failed to save table to database: {e}")

    def load_from_database(self) -> None:
        """
        Load a table from the connected database, including column data types.
        """
        if not self.ensure_connected_database():
            return

        try:
            self.table_builder.database.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in self.table_builder.database.cursor.fetchall()]

            if not tables:
                self.table_builder.system_message.create_error_message("No tables found in database.")
                return

            self.table_builder.console.print("[bold green]Available Tables:[/]")
            for idx, table in enumerate(tables, start=1):
                self.table_builder.console.print(f"{idx}. {table}")

            table_number = int(self.table_builder.input_handler.get_user_input("[bold yellow]Enter the number of the table to load[/]: ")) - 1
            
            if table_number is None:
                return
            
            if not (0 <= table_number < len(tables)):
                self.table_builder.system_message.create_error_message("Invalid table number.")
                return

            table_name = tables[table_number]
            quoted_table_name = f'"{table_name}"'

            # Fetch column information
            self.table_builder.database.cursor.execute(f"PRAGMA table_info({quoted_table_name})")
            columns_info = self.table_builder.database.cursor.fetchall()

            # Map SQL types back to program types
            sql_to_program_types = {
                "TEXT": "str",
                "INTEGER": "int",
                "REAL": "float",
                "BOOLEAN": "bool"
            }
            columns = [{"name": col[1], "type": sql_to_program_types.get(col[2].upper(), "str")} for col in columns_info]

            # Fetch rows
            self.table_builder.database.cursor.execute(f"SELECT * FROM {quoted_table_name}")
            raw_rows = self.table_builder.database.cursor.fetchall()

            # Convert rows to dictionaries and handle boolean conversion
            rows = []
            for raw_row in raw_rows:
                row = {}
                for idx, column in enumerate(columns):
                    value = raw_row[idx]
                    if column["type"] == "bool":
                        value = bool(value)  # Convert 1/0 to True/False
                    row[column["name"]] = value
                rows.append(row)

            self.table_builder.table_data["columns"] = columns
            self.table_builder.table_data["rows"] = rows

            self.table_builder.name = table_name
            self.table_builder.table_saved = True
            self.table_builder.system_message.create_information_message(
                f"Table '[bold cyan]{table_name}[/]' loaded successfully from database '[bold red]{self.table_builder.database.get_current_database()}[/]'."
            )
            if self.table_builder.settings.get_autoprint_table() == "on":
                self.table_builder.table_display.print_table()
        except Exception as e:
            self.table_builder.system_message.create_error_message(f"Failed to load table: {e}")

    def get_tables(self) -> list:
        """
        Returns a list of table names in the currently connected database.
        """
        if not self.ensure_connected_database():
            self.table_builder.system_message.create_error_message("No database is connected.")
            return []
        
        try:
            self.table_builder.database.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            return [row[0] for row in self.table_builder.database.cursor.fetchall()]
        except sqlite3.Error as e:
            self.table_builder.system_message.create_error_message(f"Failed to fetch tables [blue]{e}[/]")

    def delete_table(self) -> None:
        """
        Delete a table from the connected database by selecting it from a list of available tables.
        """
        if not self.ensure_connected_database():
            return

        try:
            # Get the list of available tables
            self.table_builder.database.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in self.table_builder.database.cursor.fetchall()]

            if not tables:
                self.table_builder.system_message.create_error_message("[bold yellow]No tables found in the database.[/]")
                return

            # Display the available tables
            self.table_builder.console.print("[bold green]Available Tables:[/]")
            for idx, table in enumerate(tables, start=1):
                self.table_builder.console.print(f"{idx}. {table}")

            # Get user selection
            table_number = int(self.table_builder.input_handler.get_user_input("[bold yellow]Enter the number of the table to delete[/]: ")) - 1

            if table_number is None:
                return

            # Validate selection
            if 0 <= table_number < len(tables):
                table_name = tables[table_number]
                quoted_table_name = f'"{table_name}"'  # Safely quote the table name

                # Confirm deletion
                confirm = self.table_builder.input_handler.get_user_input(f"[bold red]Are you sure you want to delete table '[bold cyan]{table_name}[/]'? (y/n)[/]: ").lower().strip()
                if confirm == 'y':
                    # Execute deletion
                    self.table_builder.database.cursor.execute(f"DROP TABLE {quoted_table_name}")
                    self.table_builder.database.connection.commit()
                    self.table_builder.system_message.create_information_message(f"Table '[bold cyan]{table_name}[/]' has been deleted successfully.")
                else:
                    self.table_builder.system_message.create_information_message("[bold yellow]Table deletion cancelled.[/]")
            else:
                self.table_builder.system_message.create_error_message("[bold red]Invalid table number.[/]")
        except Exception as e:
            self.table_builder.system_message.create_error_message(f"[bold red]Failed to delete table: {e}[/]")