{% macro watch_time_hrs(minutes) %}
    concat(floor({{minutes}}/60), ' hrs ', mod({{minutes}}, 60), ' mins') 

{%endmacro%}