from setuptools import setup, find_packages

setup(
    name="terminal-table-builder",
    version="1.0.0",
    description="A terminal-based table builder for CSV, JSON, Excel, PDF, and SQLite database management.",
    author="Luke Canada",
    author_email="canadaluke888@gmail.com",
    url="https://github.com/canadaluke888/TerminalTableBuilder",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "rich",
        "reportlab",
        "pdfplumber",
        "openpyxl",
        "pyexcel-ods3"
    ],
    entry_points={
        "console_scripts": [
            "terminal-table-builder=src.terminal_table.builder:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)