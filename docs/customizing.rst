Customizing your docs
======================

Descriptions
------------

To set the descriptions of each configuration item you need to specify them as comments on the same row in your
``values.yaml`` file.

.. code-block:: yaml

   image:
     repository: nginx  # docker repository to pull the image from
     tag: stable  # image tag to use
     pullPolicy: IfNotPresent  # policy for kubernetes to use when pulling images

The above YAML would be rendered like this.

.. code-block::

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
+++++

Lists will take the comment from the same line as the key. The default value will be shown as a JSON string
of the list.

.. code-block:: yaml

   env:  # environment variables
     - name: "USERNAME"
       value: "app-username"

.. code-block::

   | Parameter                | Description             | Default        |
   | ------------------------ | ----------------------- | -------------- |
   | `env` | Environment variables | `[{"name": "USERNAME", "value": "app-username"}]` |

Output formats
--------------

You can specify ``markdown``, ``rst`` or ``html`` as output formats using the ``-o`` flag. See the `command line reference`_ for more info.

.. _`command line reference`: cli.html

Templates
---------

Coming soon!