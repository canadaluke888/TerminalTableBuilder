# Terminal Table Builder

A terminal-based application that allows you to easily build and edit tabular data.

![App Screenshot](screenshots/Terminal%20Table%20Builder%20SS.png)

## Prerequisites
- Python 3.9+

## Setup
1. **Clone the repository:** `git clone https://github.com/canadaluke888/TerminalTableBuilder.git`
2. **Set up virtual environment:** For Linux and Mac OS, `python3 -m venv .venv`. For Windows, `python -m venv .venv`
3. **Activate virtual environment:** For Linux and Mac OS, `soruce .venv/bin/activate`. For Windows, `.venv/Scripts/Activate`
4. **Install requirements:** `pip install -r requirements.txt`

## Usage


### Table Builder
- **Starting the application:** For Linux and Max OS, `python3 main.py`. For Windows, `python main.py`.
- **Building a new table:** In the main menu, enter the `table builder` command. Enter a name for the table. From here you can add data to the table. Remember that the first column added is going to be the heading row each row.
- **Adding a column:** Enter the `add column` command and then enter the name for the heading.
- **Adding a row:** Enter the `add row` command and the program will walk through each heading allowing you to enter data for each cell.
- **Removing a column:** Enter the `remove column` command. Enter the column name.
- **Removing a row:** Enter the `remove row` command. Enter the row index.
- **Editing a cell:** Enter the `edit cell` command. Enter the row index. Enter the column name. Enter the new data that you want in the cell.
- **Printing the table:** Enter the `print table` command.
- **Loading data from a CSV file:** Enter the `load csv` command. Enter the path to the CSV file.
- **Saving data to a CSV file:** Enter the `save csv` command. You will be prompted on if you want to use the name of the table as the name of the CSV file. The CSV file will appear in the root directory of the app.
- **Clearning the table:** Enter the `clear table` command.
- **Renaming the table:** Enter the `rename` command. Enter the new name for the table.
- **Viewing the JSON data for the table:** Enter the `print table data` command.
- **Exiting the app:** You can you use the `exit` command to exit the application and navigate through the diffrent parts of the app.

### Settings
- **Turning on autoprint:** Once in the settings, you can enter the `autoprint_table` command. You will then be promted if you want to turn autprint on or off. Tunring on autoprint_table will automatically print the table after a change has been made.