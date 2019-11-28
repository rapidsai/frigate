import click
import frigate.gen


@click.group()
def cli():
    pass


@cli.command()
@click.argument("filename")
def gen(filename):
    frigate.gen.gen(filename)

