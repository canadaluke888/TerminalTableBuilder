#!/usr/bin/env python3

from rich.console import Console
import click
import sys
import os

console = Console()

def reconstruct_path_from_args(raw_args):
    """Attempts to reconstruct a file path if Click mistakenly splits it due to spaces."""
    fixed_args = []
    skip_next = False

    for i, arg in enumerate(raw_args):
        if skip_next:
            skip_next = False
            continue

        if arg in ("-c", "--csv", "-xl", "--xlsx", "-o", "--ods", "-p", "--pdf", "-d", "--database"):
            if i + 1 < len(raw_args) and not raw_args[i + 1].startswith("-"):
                reconstructed_path = " ".join(raw_args[i + 1:])  # Join everything after the flag
                if os.path.exists(reconstructed_path):  # Validate reconstructed path
                    fixed_args.append(arg)
                    fixed_args.append(reconstructed_path)
                    return fixed_args  # Return immediately since we fixed the path
                else:
                    console.print(f"[bold red]Error:[/] Unable to automatically fix path: {reconstructed_path}")
                    console.print("[bold yellow]Ensure you wrap paths in quotes or escape spaces with `\\`[/]")
                    sys.exit(1)

        fixed_args.append(arg)

    return fixed_args  # Return original arguments if no fix needed

# Capture and preprocess arguments BEFORE Click starts
sys.argv = reconstruct_path_from_args(sys.argv)

@click.command()
@click.option("--database", "-d", type=click.Path(file_okay=True, dir_okay=False, resolve_path=True), help="Connect to a local database and jump to the Table Builder.")
@click.option("--csv", "-c", type=click.Path(file_okay=True, dir_okay=False, resolve_path=True), help="Load a CSV file and jump to the Table Builder.")
@click.option("--xlsx", "-xl", type=click.Path(file_okay=True, dir_okay=False, resolve_path=True), help="Load an XLSX file and jump to the Table Builder.")
@click.option("--ods", "-o", type=click.Path(file_okay=True, dir_okay=False, resolve_path=True), help="Load an ODS file and jump to the Table Builder.")
@click.option("--pdf", "-p", type=click.Path(file_okay=True, dir_okay=False, resolve_path=True), help="Load a PDF file and jump to the Table Builder.")
@click.option("--tablebuilder", "-tb", is_flag=True, help="Bypass the Main Menu and jump straight to the Table Builder.")
@click.option("--settings", "-s", is_flag=True, help="Bypass the Main Menu and jump straight to the Settings.")

def main(database, csv, xlsx, ods, pdf, tablebuilder, settings):
    """ Terminal Table Builder CLI"""
    if database:
        from table_builder.builder import TableBuilder
        from settings.settings import Settings
        from database.database import Database
        console = Console()
        app_settings = Settings(console)
        database_manager = Database(console, app_settings)
        database_manager.connect(db_path=database)
        table_builder = TableBuilder(console, app_settings, database_manager)
        table_builder.launch_builder()
        return

    if csv or xlsx or ods or pdf:
        from table_builder.builder import TableBuilder
        from settings.settings import Settings
        from database.database import Database
        console = Console()
        app_settings = Settings(console)
        database_manager = Database(console, app_settings)
        table_builder = TableBuilder(console, app_settings, database_manager, name_on_start=True)

        if csv:
            table_builder.csv_handler.load_csv(path=csv)
        elif xlsx:
            table_builder.excel_handler.load_excel(path=xlsx)
        elif ods:
            table_builder.ods_handler.load_ods(path=ods)
        elif pdf:
            table_builder.pdf_handler.load_pdf(path=pdf)

        table_builder.launch_builder(print_on_start=True)
        return

    if tablebuilder:
        from table_builder.builder import TableBuilder
        from settings.settings import Settings
        from database.database import Database
        console = Console()
        app_settings = Settings(console)
        database_manager = Database(console, app_settings)
        table_builder = TableBuilder(console, app_settings, database_manager)
        table_builder.launch_builder()
        return

    if settings:
        from settings.settings import Settings
        console = Console()
        app_settings = Settings(console)
        app_settings.launch_settings()
        return

    # Launch the main menu if no arguments are provided
    from main import main as app_main
    app_main()

if __name__ == "__main__":
    try:
        main()
    except click.UsageError as e:
        console.print(f"[bold red]Click Error:[/] {e}", err=True)
        sys.exit(1)
    except click.ClickException as e:
        console.print(f"[bold red]Click Error:[/] {e}", err=True)
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Unexpected Error:[/] {e}", err=True)
        sys.exit(1)
