import click
import frigate.gen
from frigate.utils import list_templates


@click.group()
def cli():
    pass


@cli.command()
@click.argument("filename")
@click.option(
    "-o",
    "--output-format",
    "output_format",
    default="markdown",
    help="Output format for the documentation",
    type=click.Choice(list_templates()),
)
@click.option(
    "--no-credits", is_flag=True, default=True, help="Disable the Frigate credits",
)
@click.option(
    "--no-deps", is_flag=True, default=True, help="Do not render dependency values",
)
def gen(filename, output_format, no_credits, no_deps):
    click.echo(
        frigate.gen.gen(filename, output_format, credits=no_credits, deps=no_deps)
    )
