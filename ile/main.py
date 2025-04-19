from pathlib import Path

import typer

from ile.extractor import extract_transactions

app = typer.Typer()

FILE_ARG = typer.Argument(..., help="The path to the file to extract transactions from")


@app.command()
def extract(
    file: Path = FILE_ARG,
    output_format: str = "json",
):
    result = extract_transactions(file.read_text())
    if output_format == "json":
        for txn in result:
            print(txn.model_dump_json())
    else:
        print(result)


if __name__ == "__main__":
    app()
