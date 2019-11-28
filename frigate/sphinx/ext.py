from docutils import nodes
from docutils.parsers import rst

from frigate.gen import gen


class FrigateDirective(rst.Directive):
    has_content = False
    required_arguments = 1

    def run(self):
        chart_path = self.arguments[0]
        output = gen(chart_path, output_format="rst")
        return [nodes.raw(output, output, format="rst")]


def setup(app):
    app.add_directive("frigate", FrigateDirective)

