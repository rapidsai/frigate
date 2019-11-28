Frigate
===================================

.. toctree::
   :maxdepth: 2
   :hidden:

   customizing
   cli
   sphinx

Frigate is a tool for automatically generating documentation for your `Helm charts`_.

.. _`Helm charts`: https://helm.sh/

It will the chart's ``Chart.yaml`` and ``values.yaml`` files in order to
generate the content in a markup language of your choice.

Installation
------------

.. code-block:: console

   $ pip install frigate

Example
---------

Create an example ``hello-world`` Helm chart with ``helm create``.

.. code-block:: console

   $ helm create hello-world
   Creating hello-world

Run Frigate to generate markdown documentation for your new ``hello-world`` chart.

.. code-block:: console

   $ frigate gen hello-world
   hello-world
   ===========

   A Helm chart for Kubernetes

   | Parameter                | Description             | Default        |
   | ------------------------ | ----------------------- | -------------- |
   | `replicaCount` |  | `1` |
   | `image.repository` |  | `"nginx"` |
   | `image.tag` |  | `"stable"` |
   | `image.pullPolicy` |  | `"IfNotPresent"` |
   | `imagePullSecrets` |  | `[]` |
   | `nameOverride` |  | `""` |
   | `fullnameOverride` |  | `""` |
   | `service.type` |  | `"ClusterIP"` |
   | `service.port` |  | `80` |
   | `ingress.enabled` |  | `false` |
   | `ingress.annotations` |  | `{}` |
   | `ingress.hosts` |  | `[{"host": "chart-example.local", "paths": []}]` |
   | `ingress.tls` |  | `[]` |
   | `resources` |  | `{}` |
   | `nodeSelector` |  | `{}` |
   | `tolerations` |  | `[]` |
   | `affinity` |  | `{}` |

Your documentation will be piped into your stdout. You could redirect this into a file like ``README.md``.