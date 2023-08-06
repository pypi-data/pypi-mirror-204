import os
from importlib import metadata

import requests
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()
__version__ = metadata.version(__package__)

API_KEY = os.environ["BYTESIZED_API_KEY"]
BASE_URL = f"https://bytesized-hosting.com/api/v1/accounts.json?api_key={API_KEY}"


def version_callback(value: bool) -> None:
    if value:
        print(__version__)
        raise typer.Exit()


@app.callback()
def callback(
    _: bool = typer.Option(None, "--version", "-v", callback=version_callback)
) -> None:
    """Bytesized Hosting CLI App"""


def get_account_info(attribute: str):
    return requests.get(BASE_URL).json()[0][attribute]


@app.command()
def servername() -> None:
    """Name of serverd"""
    console.print(
        f'[magenta]Server name:[/magenta] [green]{get_account_info("server_name")}[/green]'
    )


@app.command()
def diskquota() -> None:
    """Disk usage quota"""
    console.print(
        f'[magenta]Disk Quota:[/magenta] [green]{get_account_info("pretty_disk_quota")}[/green]'
    )


@app.command()
def bandwidthquota() -> None:
    """Bandwidth usage quota"""
    console.print(
        f'[magenta]Bandwidth Quota:[/magenta] [green]{get_account_info("pretty_bw_quota")}[/green]'
    )


@app.command()
def memoryusage() -> None:
    """Memory usage"""
    console.print(
        f'[magenta]Memory Usage:[/magenta] [green]{round(get_account_info("memory_usage") / 1024, 2)} MB [/green]'
    )


@app.command()
def summary() -> None:
    """Summary of server"""
    response = requests.get(BASE_URL).json()[0]
    table = Table(
        show_header=False,
        show_lines=False,
        title=f"Server Summary - [purple]{response['server_name']}[/purple]",
    )
    table.add_row(
        f"[magenta]Disk Quota[/magenta]",
        f"[green]{response['pretty_disk_quota']}[/green]",
    )
    table.add_row(
        f"[magenta]Bandwidth Quota[/magenta]",
        f"[green]{response['pretty_bw_quota']}[/green]",
    )
    table.add_row(
        f"[magenta]Memory Usage[/magenta]",
        f"[green]{round(response['memory_usage'] / 1024, 2)} MB[/green]",
    )
    console.print(table)
