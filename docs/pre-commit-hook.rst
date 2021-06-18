Pre-commit hook
================


Usage with the pre-commit git hooks framework
----------------------------------------------

**Frigate** can be included as a hook for pre-commit. The easiest way to get started is to add this configuration to your ``.pre-commit-config.yaml``:


.. code-block:: yaml

   repos:
   - repo: https://github.com/rapidsai/frigate/
     rev: v0.4.0 #  pre-commit autoupdate  - to keep the version up to date
     hooks:
       - id: frigate


Parameters
----------

You can add extra parameters with :

.. code-block:: yaml

   repos:
   - repo: https://github.com/rapidsai/frigate/
      rev: v0.4.0 #  pre-commit autoupdate  - to keep the version up to date
      hooks:
         - id: frigate
         args:
         - --output=README.rst
         - --format=rst
         - --no-credits
         - --no-deps
