from pathlib import Path

import typer

from ile.extractor import extract_transactions


app = typer.Typer()


@app.command()
def extract(file: Path):
    print(extract_transactions(file.read_text()))


if __name__ == "__main__":
    app()

