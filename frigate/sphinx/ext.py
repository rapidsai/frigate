"""Module that will be used for Sphinx directive frigate."""
import pathlib

from docutils import nodes
from docutils.parsers import rst

from docutils.parsers.rst.directives import unchanged
from docutils.statemachine import ViewList

from sphinx.util.nodes import nested_parse_with_titles
from loguru import logger

from frigate.gen import gen


class FrigateDirective(rst.Directive):
    """A factory for the FrigateDirective directive.

    Args:
        rst ([type]): [description]
    """

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
            output_format=self.options.get('output_format'))
        logger.warning(gen_output)
        output = ViewList(gen_output)
        logger.error(gen_output)

        node = nodes.section()
        node.document = self.state.document
        nested_parse_with_titles(self.state, output, node)

        return node.children


def setup(app):
    """Register the directive for the sphinx application.

    Args:
        app ([SphinxApp]): The current SphinxApp
    """
    app.add_directive("frigate", FrigateDirective)
