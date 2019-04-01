{% load webcamp %}# {{ workshop.page_title }}

{% if workshop.starts_at %}Starts at: {{ workshop.starts_at|date:"l, Y-m-d @ H:i" }}
{% endif %}Duration: {{ workshop.duration_hours }} h
Skill level: {{ workshop.skill_level }}

---

{{ workshop.about|wordwrap:80 }}

{{ workshop.abstract|wordwrap:80 }}
{% for applicant in workshop.applicants.all %}
## Speaker: {{ applicant }}

{{ applicant.biography|wordwrap:80 }}
{% endfor %}
