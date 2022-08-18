"""Module that will be used for Sphinx directive frigate."""
import pathlib

from docutils.parsers.rst.directives import unchanged
from docutils.statemachine import StringList

from sphinx.util.docutils import nodes
from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import nested_parse_with_titles
from loguru import logger

from frigate.gen import gen


class FrigateDirective(SphinxDirective):
    """A factory for the FrigateDirective directive."""

    has_content = True
    required_arguments = 1
    option_spec = {
        'output_format': unchanged,
        'deps': unchanged,
    }

    def run(self):
        """Parse the source documentation.

        Returns:
            list: A list of child nodes.Node objects.
        """
        logger.debug(__name__)
        chart_path = pathlib.Path(
            f'{pathlib.Path.cwd()}/{self.arguments[0]}/').resolve()

        gen_output = gen(
            chart_path,
            deps=self.options.get('deps'),
            output_format=self.options.get('output_format')).split('\n')
        output = StringList(gen_output, source=f'{chart_path}/doc/README.md')

        node = nodes.section()
        node.document = self.state.document
        logger.debug({'output': output, 'node': node, 'document': self.state.document})

        nested_parse_with_titles(self.state, output, node)
        return node.children


def setup(app):
    """Register the directive for the sphinx application.

    Args:
        app ([SphinxApp]): The current SphinxApp
    """
    app.add_directive("frigate", FrigateDirective)
