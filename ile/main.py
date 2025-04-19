from pathlib import Path

import typer

from ile.extractor import extract_transactions

app = typer.Typer()

FILE_ARG = typer.Argument(..., help="The path to the file to extract transactions from")


@app.command()
def extract(
    file: Path = FILE_ARG,
):
    print(extract_transactions(file.read_text()))


if __name__ == "__main__":
    app()
