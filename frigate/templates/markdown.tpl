| Parameter                | Description             | Default        |
| ------------------------ | ----------------------- | -------------- |
{% for (param, comment, default) in values -%}
| `{{ param }}` | {{ comment }} | {{ default }} |
{% endfor -%}