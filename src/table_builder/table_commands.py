class TableCommands:

    def __init__(self, table_builder):
        self.table_builder = table_builder

    def run(self) -> None:
        """
        Launches the table builder loop.
        """

        if self.table_builder.settings.get_setting("hide_instructions") == "off":
            self.table_builder.instruction_message.print_table_builder_instructions()

        while True:
            builder_command = self.table_builder.console.input("[bold red]Table Builder[/] - [bold yellow]Enter a command[/]: ").lower().strip()

            if builder_command == "print help":
                self.table_builder.instruction_message.print_table_builder_instructions()

            elif builder_command == "add column":
                self.table_builder.table_operations.add_column()

                if self.table_builder.settings.get_setting("autoprint_table") == "on":
                    self.table_builder.table_display.print_table()

                if self.table_builder.settings.get_setting("auto_update") == "on":
                    self.table_builder.database_handler.save_to_database()

            elif builder_command == "change type":
                self.table_builder.table_operations.change_column_type()
                if self.table_builder.settings.get_setting("autoprint_table") == "on":
                    self.table_builder.table_display.print_table()

                if self.table_builder.settings.get_setting("auto_update") == "on":
                    self.table_builder.database_handler.save_to_database()

            elif builder_command == "rename column":
                self.table_builder.table_operations.edit_column_name()

                if self.table_builder.settings.get_setting("autoprint_table") == "on":
                    self.table_builder.table_display.print_table()

                if self.table_builder.settings.get_setting("auto_update") == "on":
                    self.table_builder.database_handler.save_to_database()

            elif builder_command == "add row":
                self.table_builder.table_operations.add_row()
                if self.table_builder.settings.get_setting("autoprint_table") == "on":
                    self.table_builder.table_display.print_table()

                if self.table_builder.settings.get_setting("auto_update") == "on":
                    self.table_builder.database_handler.save_to_database()

            elif builder_command == "edit cell":
                self.table_builder.table_operations.edit_cell()
                if self.table_builder.settings.get_setting("autoprint_table") == "on":
                    self.table_builder.table_display.print_table()

                if self.table_builder.settings.get_setting("auto_update") == "on":
                    self.table_builder.database_handler.save_to_database()

            elif builder_command == "remove column":
                self.table_builder.table_operations.remove_column()
                if self.table_builder.settings.get_setting("autoprint_table") == "on":
                    self.table_builder.table_display.print_table()

                if self.table_builder.settings.get_setting("auto_update") == "on":
                    self.table_builder.database_handler.save_to_database()

            elif builder_command == "remove row":
                self.table_builder.table_operations.remove_row()
                if self.table_builder.settings.get_setting("autoprint_table") == "on":
                    self.table_builder.table_display.print_table()

                if self.table_builder.settings.get_setting("auto_update") == "on":
                    self.table_builder.database_handler.save_to_database()

            elif builder_command == "print table":
                self.table_builder.table_display.print_table()

            elif builder_command == "print table data":
                self.table_builder.table_display.print_table_data()

            elif builder_command == "current table":
                self.table_builder.table_display.show_current_table()

            elif builder_command == "clear table":
                self.table_builder.table_operations.clear_table()

            elif builder_command == "rename":
                self.table_builder.name = self.table_builder.table_operations.name_table()
                if self.table_builder.settings.get_setting("autoprint_table") == "on":
                    self.table_builder.table_display.print_table()

                if self.table_builder.settings.get_setting("auto_update") == "on":
                    self.table_builder.database_handler.save_to_database()

            elif builder_command == "load table":
                self.table_builder.database_handler.load_from_database()
                
            elif builder_command == "save table":
                self.table_builder.database_handler.save_to_database()

            elif builder_command == "delete table":
                self.table_builder.database_handler.delete_table()
                
            elif builder_command == "load csv":
                self.table_builder.csv_handler.load_csv()

            elif builder_command == "load xl":
                self.table_builder.excel_handler.load_excel()

            elif builder_command == "load ods":
                self.table_builder.ods_handler.load_ods()
                
            elif builder_command == "load csv batch":
                self.table_builder.csv_handler.load_batch_csv()
            
            elif builder_command == "list tables":
                self.table_builder.table_display.list_tables()

            elif builder_command == "save csv":
                self.table_builder.csv_handler.save_csv()

            elif builder_command == "save xl":
                self.table_builder.excel_handler.save_excel()

            elif builder_command == "save ods":
                self.table_builder.ods_handler.save_ods()
                
            elif builder_command == "save pdf":
                self.table_builder.pdf_handler.save_pdf()
            
            elif builder_command == "load pdf":
                self.table_builder.pdf_handler.load_pdf()

            elif builder_command == "save json":
                self.table_builder.json_handler.save_json()

            elif builder_command == "help":
                self.table_builder.instruction_message.print_table_builder_instructions()

            elif builder_command == "exit":
                if not self.table_builder.table_saved:
                    exit_response = self.table_builder.console.input("[bold red]Are you sure you want to exit without saving? (y/n)[/]: ").lower().strip()
                    
                    if exit_response == "y":
                        break
                    elif exit_response == "n":
                        continue
                    else:
                        self.table_builder.system_message.create_error_message("Invalid input.")
                        
                else:
                    break

            else:
                self.table_builder.system_message.create_error_message("Invalid Command.")
                self.table_builder.autocomplete.suggest_command(builder_command, self.table_builder.autocomplete.table_builder_commands)