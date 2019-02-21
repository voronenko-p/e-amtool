{{ count }} Total Alerts

{{ criteria.active }} {{ criteria.silenced }} {{ criteria.inhibited }} {{ criteria.unprocessed }} {{ criteria.filter }} {{ criteria.receiver }} 

{% for alert in alerts %}

{{ alert.status.inhibitedBy }}
{{ alert.status.silencedBy }}
{{ alert.status.state }}

{{ alert.receivers }}

{{ alert.startsAt }}
{{ alert.updatedAt }}
{{ alert.endsAt }}

{% for label_name, label_value in alert.labels.iteritems() %}
{{label_name}}:{{label_value}}
{% endfor %}

{% for ann_name, ann_value in alert.annotations.iteritems() %}
{{ann_name}}:{{ann_value}}
{% endfor %}

  
{% endfor %}


