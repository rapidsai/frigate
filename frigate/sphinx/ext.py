"""Module that will be used for Sphinx directive frigate."""
import os

from docutils import nodes
from docutils.parsers import rst
from docutils.parsers.rst.directives import unchanged
from docutils.statemachine import ViewList
from sphinx.util.nodes import nested_parse_with_titles

from frigate.gen import gen


class FrigateDirective(rst.Directive):
    """A factory for the FrigateDirective directive.

    Args:
        rst ([type]): [description]
    """

    has_content = True
    required_arguments = 1
    option_spec = {
        'deps': bool,
        'output_format': unchanged,
    }

    def run(self):
        """Parse the source documentation.

        Returns:
            list: A list of child nodes.Node objects.
        """
        chart_path = os.path.join(
            os.getcwd(),  # TODO Need to find a better way to get the root of the docs
            self.arguments[0],
        )
        output = ViewList(gen(chart_path,
                              deps=self.options.get('deps'),
                              output_format=self.options.get('output_format')).split("\n"))

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
