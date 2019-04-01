{% load webcamp %}# {{ talk }}

{% if talk.starts_at %}Starts at: {{ talk.starts_at|date:"l, Y-m-d @ H:i" }}
{% endif %}Duration: {{ talk.duration }} min
Skill level: {{ talk.skill_level }}

---

{{ talk.about|wordwrap:80 }}

{{ talk.abstract|wordwrap:80 }}
{% for applicant in talk.applicants.all %}
## Speaker: {{ applicant }}

{{ applicant.biography|wordwrap:80 }}
{% endfor %}
