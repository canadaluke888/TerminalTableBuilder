import pdfplumber
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table as PDFTable, TableStyle
from reportlab.lib import colors
import os




class PDFHandler:
    def __init__(self, table_builder):
        self.table_builder = table_builder
        

    def save_pdf(self) -> None:
        """
        Save the current table data to a PDF file.
        """
        if not self.table_builder.table_data["columns"] or not self.table_builder.table_data["rows"]:
            self.table_builder.system_message.create_error_message("No table data to export to PDF.")
            return

        # Prompt for the file name
        use_table_name = self.table_builder.input_handler.get_user_input(
            "[bold yellow]Use table name as save file name? (y/n)[/]: ").strip().lower()

        if use_table_name == "y":
            file_name = f"{self.table_builder.name}.pdf"
        elif use_table_name == "n":
            file_name = self.table_builder.input_handler.get_user_input(
                "[bold yellow]Enter the name of the PDF file (without extension)[/]: ").strip() + ".pdf"
        else:
            self.table_builder.system_message.create_error_message("Invalid input.")
            return

        try:
            # Create the PDF document
            pdf = SimpleDocTemplate(file_name, pagesize=letter)
            elements = []

            # Prepare the table data for the PDF
            # Extract column names from the dictionaries
            column_headers = [column["name"] for column in self.table_builder.table_data["columns"]]
            pdf_data = [column_headers]  # Header row

            # Add row data
            for row in self.table_builder.table_data["rows"]:
                pdf_data.append([row.get(column["name"], "") for column in self.table_builder.table_data["columns"]])

            # Create the table with styling
            table = PDFTable(pdf_data)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]))

            elements.append(table)

            # Build the PDF
            pdf.build(elements)
            self.table_builder.table_saved = True
            self.table_builder.system_message.create_information_message(
                f"Table data successfully exported to '[bold cyan]{file_name}[/]'."
            )
        except Exception as e:
            self.table_builder.system_message.create_error_message(f"Failed to save table as PDF: {e}")

    def load_pdf(self, path: str | os.PathLike = None) -> None:
        """
        Load table data from a PDF file using pdfplumber.

        Args:
            path (str): Path to the PDF file. If not provided through CLI shortcut, prompt the user.
        """
        file_name = path or self.table_builder.input_handler.get_user_input("[bold yellow]Enter path to the PDF file[/]: ").strip()

        if file_name is None:
            return

        if not os.path.exists(file_name):
            self.table_builder.system_message.create_error_message("File not found.")
            return

        try:
            with pdfplumber.open(file_name) as pdf:
                extracted_data = []
                for page in pdf.pages:
                    tables = page.extract_table()
                    if tables:
                        extracted_data.extend(tables)

            if not extracted_data:
                self.table_builder.system_message.create_error_message("No table data found in the PDF.")
                return

            # Use first row as column headers
            self.table_builder.table_data["columns"] = [{"name": col, "type": "str"} for col in extracted_data[0]]
            self.table_builder.table_data["rows"] = [{col: row[i] if i < len(row) else "" for i, col in enumerate(extracted_data[0])} for row in extracted_data[1:]]
            if self.table_builder.settings.get_setting("infer_data_types") == "on":
                self.table_builder.table_specs.infer_column_types()
            self.table_builder.name = os.path.splitext(os.path.basename(file_name))[0]
            self.table_builder.system_message.create_information_message("PDF file loaded successfully.")
        except Exception as e:
            self.table_builder.system_message.create_error_message(f"Failed to load PDF file: {e}")