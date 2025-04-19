import asyncio
from pathlib import Path

import typer

from ile.extractor import extract_transactions

app = typer.Typer()

FILE_ARG = typer.Argument(..., help="The path to the file to extract transactions from")


async def async_extract(
    file: Path,
    output_format: str = "json",
):
    result = await extract_transactions(file.read_text())
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


if __name__ == "__main__":
    app()
