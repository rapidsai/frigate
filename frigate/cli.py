import click
import frigate.gen


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
    type=click.Choice(["markdown", "rst"]),
)
def gen(filename, output_format):
    click.echo(frigate.gen.gen(filename, output_format))

