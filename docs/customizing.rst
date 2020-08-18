Customizing your docs
======================

Configuration descriptions
--------------------------

To set the descriptions of each configuration item you need to specify them as comments on the same row in your
``values.yaml`` file.

.. code-block:: yaml

   image:
     repository: nginx  # docker repository to pull the image from
     tag: stable  # image tag to use
     pullPolicy: IfNotPresent  # policy for kubernetes to use when pulling images

The above YAML would be rendered like this.

.. code-block:: md

   | Parameter                | Description             | Default        |
   | ------------------------ | ----------------------- | -------------- |
   | `image.repository` | Docker repository to pull the image from | `"nginx"` |
   | `image.tag` | Image tag to use | `"stable"` |
   | `image.pullPolicy` | Policy for kubernetes to use when pulling images | `"IfNotPresent"` |

Only comments on the same line as the option will be used.

.. code-block:: yaml

   # this comment will be ignored!
   replicaCount: 1  # this comment will be used 🎉
   # this comment will also be ignored!

Lists
^^^^^

Lists will take the comment from the same line as the key. The default value will be shown as a JSON string
of the list.

.. code-block:: yaml

   env:  # environment variables
     - name: "USERNAME"
       value: "app-username"

.. code-block:: md

   | Parameter                | Description             | Default        |
   | ------------------------ | ----------------------- | -------------- |
   | `env` | Environment variables | `[{"name": "USERNAME", "value": "app-username"}]` |

Output formats
--------------

You can specify ``markdown``, ``rst`` or ``html`` as output formats using the ``-o`` flag. See the `command line reference`_ for more info.

.. _`command line reference`: cli.html

Templates
---------

Frigate uses jinja2_ templates to render your documentation.

As well as being able to specify various built in templates using the output
formats flag you may also provide your own template all together.

To do this place a valid jinja2 template in your helm chart directory named ``.frigate``. This template will then
be used instead of any built in templates.

.. code-block:: console

   $ frigate gen hello-world

If the ``hello-world`` chart contains a ``.frigate`` template file this will be used automatically.

Available variables
^^^^^^^^^^^^^^^^^^^

Frigate exposes all of the options from within your chart's ``Chart.yaml`` file as variables along with a list of tuples of all
the configuration options called ``values``.

For example you can access the ``name`` and ``version`` fields from your ``Chart.yaml``.

.. code-block:: jinja

   {{ name }} - {{ version }}

Frigate makes use of most of the `default fields`_ from your ``Chart.yaml`` in it's default templates, along with a few Frigate specific ones which you can
optionally include.

 - ``long_description`` - A multiline description of your helm chart. Useful for including installation instructions and further information.
 - ``footnotes`` - A continuation of the long description to place below your table of configuration options. Useful for documenting things which are useful but not immediately important.

A simple ``.frigate`` template could be the following.

.. code-block:: jinja

   # {{ name }} - {{ version }}

   {{ description }}

   ## Configuration options

   {% for (param, comment, default) in values -%}
    - `{{ param }}` - {{ default }}
   {% endfor -%}

This template is in markdown and would place your chart's title and version in a top level header. Then include the description followed by a list of the
configration options. It would output documentation like this.

.. code-block:: md

   # simple - 0.1.0

   A Helm chart for Kubernetes

   ## Configuration options

   - `replicaCount` - `1`
   - `image.repository` - `"nginx"`
   - `image.tag` - `"stable"`
   - `image.pullPolicy` - `"IfNotPresent"`
   - `imagePullSecrets` - `[]`
   - `nameOverride` - `""`
   - `fullnameOverride` - `""`
   - `service.type` - `"ClusterIP"`
   - `service.port` - `80`
   - `ingress.enabled` - `false`
   - `ingress.annotations` - `{}`
   - `ingress.hosts` - `[{"host": "chart-example.local", "paths": []}]`
   - `ingress.tls` - `[]`
   - `resources` - `{}`
   - `nodeSelector` - `{}`
   - `tolerations` - `[]`
   - `affinity` - `{}`



Extending built in templates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Instead of writing a whole template from scratch you are able to extend the built in charts. Specify the template
you wish to extend and the blocks within the template that you wish to override.

.. code-block:: jinja

   {% extends "markdown.jinja" %}

   {% block title -%}
   # {{ name | upper }}
   {%- endblock %}

The above example would extent the ``markdown`` template and overrides the ``title`` block with an uppercase title.

Templates available to extend:

 - ``markdown.jinja2`` - Markdown template
 - ``rst.jinja2`` - reStructuredText template
 - ``html.jinja2`` - HTML template
 - ``base.jinja2`` - Base blank template with no content

Blocks available for overriding:

 - ``header`` - Misc block for the top of the document
 - ``title`` - The title of the page
 - ``description`` - The description of the chart
 - ``table`` - The table of configuration options
 - ``footnotes`` - Additional description to go below the table
 - ``credits`` - Crediting the generation of the document to Frigate
 - ``footer`` - Misc block for the bottom of the document

.. _jinja2: https://jinja.palletsprojects.com/
.. _`default fields`: https://helm.sh/docs/topics/charts/#the-chart-yaml-file
