import os

from docutils import nodes
from docutils.parsers import rst
from docutils.parsers.rst.directives import unchanged
from docutils.statemachine import ViewList
from sphinx.util.nodes import nested_parse_with_titles

from frigate.gen import gen


class FrigateDirective(rst.Directive):
    has_content = True
    required_arguments = 1
    option_spec = {
        'output_format': unchanged,
    }

    def run(self):
        chart_path = os.path.join(
            os.getcwd(),  # TODO Need to find a better way to get the root of the docs
            self.arguments[0],
        )
        if self.options.get('output_format') is None:
            self.options.update({'output_format': 'rst'})
        output = ViewList(gen(chart_path, output_format=self.options.get('output_format')).split("\n"))

        node = nodes.section()
        node.document = self.state.document
        nested_parse_with_titles(self.state, output, node)

        return node.children


def setup(app):
    app.add_directive("frigate", FrigateDirective)
