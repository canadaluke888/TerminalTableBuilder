import sqlite3
import os
from rich.console import Console
from message_panel.system_message import SystemMessage
from message_panel.instruction_message import InstructionMessage
from autocomplete.autocomplete import Autocomplete
from rich.panel import Panel
from settings.settings import Settings

class Database:
    def __init__(self, console: Console, settings: Settings):
        """
        Initialize the Database manager.
        :param console: Console instance for rich text output.
        :param settings: Settings instance for getting user settings.
        """
        self.console = console
        self.settings = settings
        self.system_message = SystemMessage(self.console)
        self.instruction_message = InstructionMessage(self.console)
        self.autocomplete = Autocomplete(self.console)
        self.current_database = None
        self.connection = None
        self.cursor = None
        self.database_directory = os.path.join(os.getcwd(), "databases")
        self.ensure_database_directory()
        
    def search(self):
        """
        Search for a string in a specified table or all tables in the connected database.
        """
        if not self.is_connected():
            self.system_message.create_error_message("No database is connected. Please connect to a database first.")
            return

        try:
            # Prompt user for the search string
            search_string = self.console.input("[bold yellow]Enter the search query[/]: ").strip()
            if not search_string:
                self.system_message.create_error_message("Search query cannot be empty.")
                return

            # Fetch all table names in the database
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in self.cursor.fetchall()]

            if not tables:
                self.system_message.create_error_message("No tables found in the database.")
                return

            # Ask the user to specify a table or search all tables
            self.console.print("[bold green]Available Tables:[/]")
            self.console.print("[bold yellow]0. Search All Tables[/]")
            for idx, table in enumerate(tables, start=1):
                self.console.print(f"{idx}. {table}")

            table_number = int(self.console.input("[bold yellow]Enter the table number to search (or 0 for all tables)[/]: ")) - 1

            if table_number == -1:  # Search all tables
                target_tables = tables
            elif 0 <= table_number < len(tables):
                target_tables = [tables[table_number]]
            else:
                self.system_message.create_error_message("Invalid table number.")
                return

            # Perform the search
            results = []
            for table in target_tables:
                # Fetch column information with data types
                self.cursor.execute(f'PRAGMA table_info("{table}");')
                columns_info = self.cursor.fetchall()
                columns = [{"name": col[1], "type": col[2]} for col in columns_info]

                # Safely quote the table name
                quoted_table_name = f'"{table}"'
                self.cursor.execute(f"SELECT * FROM {quoted_table_name}")
                rows = self.cursor.fetchall()

                # Search each row and column for the search string
                for row_idx, row in enumerate(rows, start=1):
                    for col_idx, value in enumerate(row):
                        if search_string.lower() in str(value).lower():
                            column = columns[col_idx]
                            results.append((table, row_idx, column["name"], column["type"], value))

            # Display the results
            if not results:
                self.system_message.create_information_message(f"No matches found for '[bold cyan]{search_string}[/]'.")
                return

            self.console.print(f"[bold green]Search Results for '[bold cyan]{search_string}[/]':[/]")
            for table, row_idx, column_name, column_type, value in results:
                self.console.print(Panel(
                    f"""
[bold red]Table[/]: [bold cyan]{table}[/]

[bold red]Row[/]: [bold cyan]{row_idx}[/]

[bold red]Column[/]: [bold cyan]{column_name}[/]

[bold red]Type[/]: [bold cyan]{column_type}[/]

[bold red]Value[/]: [bold cyan]{value}[/]
                    """,
                    title="[bold red]Results[/]",
                    title_align="center",
                    border_style="cyan"))

        except sqlite3.Error as e:
            self.system_message.create_error_message(f"Search query failed: {e}")



    def ensure_database_directory(self):
        """
        Ensure the 'databases' directory exists in the current working directory.
        """
        if not os.path.exists(self.database_directory):

            startup_set = self.console.input("[bold yellow]Do you want to set a custom path for the database directory? (y/n): ").lower().strip()

            if startup_set == "y":
                directory = self.console.input("[bold yellow]Enter the path to the directory[/]: ").strip()
                databases_directory = os.path.join(directory, "databases")
                self.settings.set_database_directory(databases_directory)
                self.system_message.create_information_message(f"Created 'databases' directory at [bold red]{databases_directory}[/]")
            elif startup_set == "n" or None:
                os.makedirs(self.database_directory)
                self.settings.set_database_directory(self.database_directory)
                self.system_message.create_information_message(f"Created 'databases' directory at [bold red]{self.database_directory}[/]")
            
    def connect(self, db_name: str = None, db_path: str = None):
        """
        Connect to the specified SQLite database. Supports both a database name (within the 'databases' directory)
        or a full file path.

        :param db_name: Name of the database (inside the 'databases' directory).
        :param db_path: Full path to the database file.
        """
        if db_path:
            # Use the provided full path
            resolved_path = os.path.abspath(db_path)
        elif db_name:
            # Construct path using the 'databases' directory
            resolved_path = os.path.join(self.database_directory, db_name)
        else:
            self.system_message.create_error_message("No database name or path provided.")
            return

        if not os.path.exists(resolved_path):
            self.system_message.create_error_message(f"Database '[bold cyan]{resolved_path}[/]' does not exist.")
            return

        try:
            self.connection = sqlite3.connect(resolved_path)
            self.cursor = self.connection.cursor()
            self.current_database = resolved_path
            self.system_message.create_information_message(f"Connected to database: [bold cyan]{resolved_path}[/]")
        except sqlite3.Error as e:
            self.system_message.create_error_message(f"Failed to connect to database: {e}")


    def close(self) -> None:
        """
        Close the current database connection.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
            self.current_database = None
            self.system_message.create_information_message("Database connection closed.")

    def get_current_database(self):
        """
        Get the name of the currently connected database.
        """
        return self.current_database

    def is_connected(self):
        """
        Check if a database is currently connected.
        """
        return self.connection is not None

    def create_database(self, db_name: str):
        """
        Create a new SQLite database in the 'databases' directory.
        """
        db_path = os.path.join(self.database_directory, db_name)
        if os.path.exists(db_path):
            self.system_message.create_error_message("Database already exists. Connect instead.")
            return
        try:
            open(db_path, 'w').close()  # Create an empty file
            self.system_message.create_information_message(f"Database created: [bold cyan]{db_name}[/]")
            self.connect(db_name)
        except Exception as e:
            self.system_message.create_error_message(f"Failed to create database: {e}")

    def delete_database(self, db_name: str):
        """
        Delete the specified SQLite database from the 'databases' directory.
        """
        db_path = os.path.join(self.database_directory, db_name)
        if not os.path.exists(db_path):
            self.system_message.create_error_message("Database does not exist.")
            return
        try:
            os.remove(db_path)
            self.system_message.create_information_message(f"Database deleted: [bold cyan]{db_name}[/]")
            if self.current_database == db_name:
                self.close()
        except Exception as e:
            self.system_message.create_error_message(f"Failed to delete database: {e}")

    def list_databases(self):
        """
        List all SQLite databases in the 'databases' directory.
        """
        databases = [f for f in os.listdir(self.database_directory) if f.endswith('.db')]
        if not databases:
            self.system_message.create_error_message("No databases found.")
            return []

        self.console.print("[bold green]Available Databases:[/]")
        for idx, db in enumerate(databases, start=1):
            self.console.print(f"{idx}. {db}")
        return databases

    def select_database(self):
        """
        Allow the user to select a database from the 'databases' directory.
        """
        databases = self.list_databases()
        if not databases:
            return

        try:
            db_number = int(self.console.input("[bold yellow]Select a database number[/]: ")) - 1
            if 0 <= db_number < len(databases):
                self.connect(databases[db_number])
            else:
                self.system_message.create_error_message("Invalid database number.")
        except ValueError:
            self.system_message.create_error_message("Invalid input. Please enter a valid number.")

    def launch_database(self):
        """
        Interactive interface for managing databases.
        """

        if self.settings.get_setting("hide_instructions") == "off":
            self.instruction_message.print_database_instructions()
            
        while True:
            command = self.console.input(
                "[bold red]Database Manager[/] - [bold yellow]Enter a command[/]: "
            ).strip().lower()

            if command == "create database":
                db_name = self.console.input(
                    "[bold yellow]Enter the name for the new database (without .db)[/]: "
                ) + ".db"
                self.create_database(db_name)

            elif command == "delete database":
                db_name = self.console.input(
                    "[bold yellow]Enter the name of the database to delete (without .db)[/]: "
                ) + ".db"
                self.delete_database(db_name)

            elif command == "list databases":
                self.list_databases()

            elif command == "select database":
                self.select_database()

            elif command == "current database":
                self.system_message.create_information_message(f"Current database: [bold cyan]{self.current_database}[/]")

            elif command == "close database":
                self.close()
                
            elif command == "search":
                self.search()

            elif command == "help":
                self.instruction_message.print_database_instructions()

            elif command == "exit":
                break

            else:
                self.system_message.create_error_message("Invalid input.")
                self.autocomplete.suggest_command(command, self.autocomplete.database_commands)
