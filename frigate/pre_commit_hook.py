import os
from pathlib import Path

from frigate.gen import gen


def main(output_file, format, credits, deps):
    """Write a README file for discovered Helm chart(s).


    Args:
        output_file (str): Basename of the file to generate
        output_format (str): Output format (maps to jinja templates in frigate)
        credits (bool): Show Frigate credits in documentation
        deps (bool): Read values from chart dependencies and include them in the config table

    Returns:
        int: How many files were updated by the hook

    """
    dirs = []
    path = os.getcwd()
    name = "Chart.yaml"

    retval = 0
    charts = []

    # Find all the charts
    for root, dirs, files in os.walk(path):
        if name in files:
            charts.append(os.path.join(root, name))

    # For each chart
    for chart in charts:
        chart_location = os.path.dirname(chart)
        frigate_output = gen(chart_location, format, credits=credits, deps=deps)
        artifact = Path(chart_location, output_file)
        Path(artifact).touch()
        with open(artifact, "r") as before:
            current_output = before.read()
        if current_output != frigate_output:
            retval += 1
            with open(artifact, "w") as generated:
                generated.write(frigate_output)
    return retval
