{% macro apply_retention(target_relation) %}
  {{ return(adapter.dispatch('apply_retention', 'dbt')(target_relation)) }}
{%- endmacro -%}

{% macro spark__apply_retention(relation) %}
  {%- set file_format = config.get('file_format', 'openhouse') -%}
  {%- set granularity = config.get('partition_granularity', none) -%}
  {%- set retention = config.get('retention_period', none) -%}

  {% if file_format == 'openhouse' %}
    {% if config.get('partition_by', none) is not none and granularity is not none %}
        {% set retention_query %}
        {% if retention is not none %}
            alter table {{ relation }} set policy (RETENTION={{ retention }})
        {% else %}
            {% if granularity == 'hours' %}
                alter table {{ relation }} set policy (RETENTION=8760h)
            {% elif granularity == 'days' %}
                alter table {{ relation }} set policy (RETENTION=365d)
            {% elif granularity == 'months' %}
                alter table {{ relation }} set policy (RETENTION=12m)
            {% else %}
                alter table {{ relation }} set policy (RETENTION=1y)
            {% endif %}
        {% endif %}
        {% endset %}
        {% do run_query(retention_query) %}
    {% endif %}
  {%- else -%}
    {{ exceptions.raise_compiler_error("Invalid configs for 'retention_period'. Retention config is not supported for this file_format: " ~ file_format) }}
  {% endif %}
{%- endmacro -%}
