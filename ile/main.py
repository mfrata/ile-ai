import asyncio
from pathlib import Path

import typer

from ile.extractor import extract_transactions
from ile.ui import start_ui

app = typer.Typer()

FILE_ARG = typer.Argument(..., help="The path to the file to extract transactions from")


async def async_extract(
    file: Path,
    output_format: str = "json",
):
    media_type = "application/pdf" if file.suffix == ".pdf" else "text/csv"
    content = file.read_bytes()
    result = await extract_transactions(content, media_type)
    if output_format == "json":
        for txn in result:
            print(txn.model_dump_json())
    else:
        print(result)


@app.command()
def extract(
    file: Path = FILE_ARG,
    output_format: str = "json",
):
    asyncio.run(async_extract(file, output_format))


@app.command()
def ui():
    start_ui()


if __name__ == "__main__":
    app()
