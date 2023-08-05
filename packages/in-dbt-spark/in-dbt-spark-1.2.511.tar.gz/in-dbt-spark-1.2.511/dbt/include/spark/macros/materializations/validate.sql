{% macro dbt_spark_validate_get_file_format(raw_file_format) %}
  {#-- Validate the file format #}

  {% set accepted_formats = ['text', 'csv', 'json', 'jdbc', 'parquet', 'orc', 'hive', 'delta', 'libsvm', 'hudi', 'openhouse'] %}

  {% set invalid_file_format_msg -%}
    Invalid file format provided: {{ raw_file_format }}
    Expected one of: {{ accepted_formats | join(', ') }}
  {%- endset %}

  {% if raw_file_format not in accepted_formats %}
    {% do exceptions.raise_compiler_error(invalid_file_format_msg) %}
  {% endif %}

  {% do return(raw_file_format) %}
{% endmacro %}


{% macro dbt_spark_validate_get_incremental_strategy(raw_strategy, file_format) %}
  {#-- Validate the incremental strategy #}

  {% set invalid_strategy_msg -%}
    Invalid incremental strategy provided: {{ raw_strategy }}
    Expected one of: 'append', 'merge', 'insert_overwrite'
  {%- endset %}

  {% set invalid_merge_msg -%}
    Invalid incremental strategy provided: {{ raw_strategy }}
    You can only choose this strategy when file_format is set to 'delta' or 'hudi'
  {%- endset %}

  {% set invalid_insert_overwrite_delta_msg -%}
    Invalid incremental strategy provided: {{ raw_strategy }}
    You cannot use this strategy when file_format is set to 'delta'
    Use the 'append' or 'merge' strategy instead
  {%- endset %}

  {% set invalid_insert_overwrite_endpoint_msg -%}
    Invalid incremental strategy provided: {{ raw_strategy }}
    You cannot use this strategy when connecting via endpoint
    Use the 'append' or 'merge' strategy instead
  {%- endset %}

  {% if raw_strategy not in ['append', 'merge', 'insert_overwrite'] %}
    {% do exceptions.raise_compiler_error(invalid_strategy_msg) %}
  {%-else %}
    {% if raw_strategy == 'merge' and file_format not in ['delta', 'hudi'] %}
      {% do exceptions.raise_compiler_error(invalid_merge_msg) %}
    {% endif %}
    {% if raw_strategy == 'insert_overwrite' and file_format == 'delta' %}
      {% do exceptions.raise_compiler_error(invalid_insert_overwrite_delta_msg) %}
    {% endif %}
    {% if raw_strategy == 'insert_overwrite' and target.endpoint %}
      {% do exceptions.raise_compiler_error(invalid_insert_overwrite_endpoint_msg) %}
    {% endif %}
  {% endif %}

  {% do return(raw_strategy) %}
{% endmacro %}

{% macro dbt_spark_validate_openhouse_configs(file_format) %}
  {#-- Validate against configs that OpenHouse does not support ahead of time #}

  {% if file_format == 'openhouse' %}

    {% if config.get('clustered_by', none) is not none %}
      {% do exceptions.raise_compiler_error("'clustered_by' is not supported for 'openhouse' file_format") %}
    {% endif %}

    {% if config.get('location_root', none) is not none %}
      {% do exceptions.raise_compiler_error("'location_root' is not supported for 'openhouse' file_format") %}
    {% endif %}

    {% if config.get('partition_by', none) is not none %}
      {% set granularity = config.get('partition_granularity', none) %}
      {% if granularity is none %}
        {% do exceptions.raise_compiler_error("For partitioned tables with file_format = 'openhouse', 'partition_granularity' must be supplied.") %}
      {% endif %}
      {% if granularity not in ['days', 'hours', 'months', 'years'] %}
        {% do exceptions.raise_compiler_error("For partitioned tables with file_format = 'openhouse', 'partition_granularity' must be one of ('hours', 'days', 'months', or 'years').") %}
      {% endif %}
    {% endif %}

    {%- set grant_config = config.get('grants', none) -%}
    {%- if grant_config is not none %}
        {%- for privilege in grant_config.keys() %}
          {% if privilege.lower() not in ['select', 'manage grants'] %}
            {% do exceptions.raise_compiler_error("For outputs with file_format = 'openhouse', keys in 'grants' map must be one of ('select', 'manage_grants').") %}
          {% endif %}
        {%- endfor -%}
    {% endif %}

    {% if config.get('retention_period', none) is not none %}
      {% if config.get('partition_by', none) is none %}
        {% do exceptions.raise_compiler_error("For tables with file_format = 'openhouse' and 'retention_period', 'partition_by' must be supplied") %}
      {% endif %}
    {% endif %}
  {% endif %}

  {% do return(file_format) %}
{% endmacro %}
