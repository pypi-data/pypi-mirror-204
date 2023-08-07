import logging
import re
import subprocess as sp
import click
from rich.console import Console
from rich.table import Table

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

RE_DATASETS = re.compile(
    r"Dataset (?P<dataset>[\w._\-\/@]+) \[ZPL\], ID (?P<id>\d+), cr_txg (?P<cr_txg>\d+), (?P<size>\d+), (?P<objects>\d+) objects"
)

console = Console()

def execute(command):
    return sp.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        check=True
    ).stdout

@click.command()
@click.argument("dataset")
def cli(dataset):
    result = execute(f"zdb -P -d {dataset}")
    logging.debug(result)

    datasets = re.findall(RE_DATASETS, result)
    logging.debug(datasets)

    if len(datasets) == 0:
        logging.info("No datasets.")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Dataset")
    table.add_column("Size")
    table.add_column("Objects", justify="right")

    for dataset in datasets:
        table.add_row(dataset[0], dataset[3], dataset[4])

    console.print(table)

if __name__ == "__main__":
    cli()
