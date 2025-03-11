from rich.console import Console
from settings.settings import Settings
from database.database import Database
from message_panel.system_message import SystemMessage
from message_panel.instruction_message import InstructionMessage
from autocomplete.autocomplete import Autocomplete
from .io.pdf_handler import PDFHandler
from .io.csv_handler import CSVHandler
from .io.excel_handler import ExcelHandler
from .io.ods_handler import ODSHandler
from .io.json_handler import JSONHandler
from .database_handler import DatabaseHandler
from .table_operations import TableOperations
from .table_display import TableDisplay
from .utils import InputHandler, TableSpecs

class TableBuilder:

    def __init__(self, console: Console, settings: Settings, database: Database, name_on_start: bool = False):
        self.console = console
        self.database = database
        self.settings = settings
        self.system_message = SystemMessage(console)
        self.instruction_message = InstructionMessage(console)
        self.autocomplete = Autocomplete(console)

        self.csv_handler = CSVHandler(self)
        self.json_handler = JSONHandler(self)
        self.pdf_handler = PDFHandler(self)
        self.excel_handler = ExcelHandler(self)
        self.ods_handler = ODSHandler(self)
        self.database_handler = DatabaseHandler(self)
        self.table_operations = TableOperations(self)
        self.table_display = TableDisplay(self)
        self.input_handler = InputHandler(self)
        self.table_specs = TableSpecs(self)

        
        if not name_on_start:
            self.name = self.table_operations.name_table()
        self.table_data = {"columns": [], "rows": []}
        self.table_saved = False


    def launch_builder(self, print_on_start: bool = False):
        from .table_commands import TableCommands
        TableCommands(self).run(print_on_start=print_on_start)
