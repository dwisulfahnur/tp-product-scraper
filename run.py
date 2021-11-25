#!python

import os
import sys
import csv
import time
import typer
from pathlib import Path
from src.common.exceptions import NoProductsFound
from src.tokopedia.helpers import get_products
from pathlib import Path
from typing import Optional
from src.common.config import BASE_DIR


app = typer.Typer(add_completion=False)


@app.callback(invoke_without_command=True)
def main(
        category: str = typer.Option(..., '-c', '--category'),
        length: int = typer.Option(..., '-l', '--length'),
        output: Optional[Path] = typer.Option('output', '-o', '--output'),
):
    try:
        products = get_products(category, length)
    except NoProductsFound:
        typer.echo(typer.style(
            f"There is No Product Found for the '{category}' Category", fg=typer.colors.RED))
        sys.exit()

    output_dir = os.path.join(BASE_DIR, output)
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    filename = f"{category.split('/')[-1]}_{length}_{int(time.time())}.csv"
    csv_file = open(os.path.join(output_dir, filename), 'w')
    csv_writer = csv.writer(csv_file)
    header = products[0].keys()
    csv_writer.writerow([head.capitalize() for head in header])
    for product in products:
        item = [product[key] for key in header]
        csv_writer.writerow(item)

    csv_file.close()
    typer.echo("Done!")


if __name__ == '__main__':
    app()
