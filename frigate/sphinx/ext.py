import os

from docutils import nodes
from docutils.parsers import rst
from docutils.statemachine import ViewList
from sphinx.util.nodes import nested_parse_with_titles

from frigate.gen import gen


class FrigateDirective(rst.Directive):
    has_content = False
    required_arguments = 1

    def run(self):
        chart_path = os.path.join(
            os.getcwd(),  # TODO Need to find a better way to get the root of the docs
            self.arguments[0],
        )
        output = ViewList(gen(chart_path, output_format="rst").split("\n"))

        node = nodes.section()
        node.document = self.state.document
        nested_parse_with_titles(self.state, output, node)

        return node.children


def setup(app):
    app.add_directive("frigate", FrigateDirective)
