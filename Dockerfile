# Use an official Python image
FROM python:3.9

# Set working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . .

RUN pip install -r requirements.txt

# Set execute permission for the script
RUN chmod +x /app/terminal_table_builder.py

# Ensure the script is executed as a Python script
ENTRYPOINT ["python3", "/app/terminal_table_builder.py"]
