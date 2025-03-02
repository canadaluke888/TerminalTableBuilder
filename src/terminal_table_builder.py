#!/user/bin/env python3


import argparse
from rich.console import Console
from src.message_panel.system_message import SystemMessage
from table_builder.builder import TableBuilder
from settings.settings import Settings
from database.database import Database


def main():
    console = Console()
    system_message = SystemMessage(console)
    settings = Settings(console)
    database = Database(console, settings)

    parser = argparse.ArgumentParser(description="Terminal Table Builder CLI")
    parser.add_argument("--database", "-d", help="Specify a database to connect to.")
    parser.add_argument(
        "--csv", "-c", help="Load a CSV file and jump to the Table Builder."
    )
    parser.add_argument(
        "--xlsx", "-xl", help="Load a XLSX file and jump to the Table Builder."
    )
    parser.add_argument(
        "--ods", "-o", help="Load a ODS file and jump to the Table Builder."
    )
    parser.add_argument(
        "--pdf", "-p",
        help="Load a PDF file and jump straight to the Table Builder."
    )
    parser.add_argument(
        "--tablebuilder",
        "-tb",
        help="Bypass Main Menu and jump straight to the Table Builder.",
    )
    parser.add_argument(
        "--settings", "-s",
        help="Bypass the Main Menu and jump straight to the Settings."
    )

    args = parser.parse_args()

    if args.database:
        database.connect(args.database)
        if database.is_connected():
            system_message.create_information_message(
                f"Connected to database: {args.database}"
            )

    # Load Shortcuts
    if args.csv:
        table_builder = TableBuilder(console, settings, database, print_on_start=True)
        table_builder.csv_handler.load_csv(path=args.csv)
        table_builder.launch_builder()
        return

    if args.xlsx:
        table_builder = TableBuilder(console, settings, database, print_on_start=True)
        table_builder.excel_handler.load_excel(path=args.xlsx)
        table_builder.launch_builder()
        return

    if args.ods:
        table_builder = TableBuilder(console, settings, database, print_on_start=True)
        table_builder.ods_handler.load_ods(path=args.ods)
        table_builder.launch_builder()
        return
    
    if args.pdf:
        table_builder = TableBuilder(console, settings, database, print_on_start=True)
        table_builder.pdf_handler.load_pdf(args.pdf)
        table_builder.launch_builder()
        return

    # Menu Shortcuts
    if args.tablebuilder:
        table_builder = TableBuilder(
            console, settings, database, name_on_start=args.tablebuilder
        )
        table_builder.launch_builder()
        return
    
    if args.settings:
        settings.launch_settings()
        return
    

    # Launch the main menu if no arguments are provided
    from src.main import main as app_main

    app_main()


if __name__ == "__main__":
    main()
