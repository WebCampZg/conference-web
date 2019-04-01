# {{ post.title }}

Published at {{ post.created_at }}

{{ post.lead|striptags|safe|wordwrap:80 }}

{{ post.body|striptags|safe|wordwrap:80 }}
