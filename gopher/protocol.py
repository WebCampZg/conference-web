import re

from blog.models import Post
from config.utils import get_active_event
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from pages.models import Page
from talks.models import Talk
from textwrap import wrap
from twisted.internet import protocol
from workshops.models import Workshop

site = Site.objects.get_current()
domain = site.domain.split(":")[0]
event = get_active_event()


class Gopher(protocol.Protocol):
    @property
    def port(self):
        return self.transport.server.port

    def file_item(self, title, id):
        line = f"0{title}\t{id}\t{domain}\t{self.port}\r\n"
        self.transport.write(line.encode())

    def menu_item(self, title, id):
        line = f"1{title}\t{id}\t{domain}\t{self.port}\r\n"
        self.transport.write(line.encode())

    def write_line(self, line):
        self.transport.write(line.encode())
        self.transport.write(b"\r\n")

    def write_text(self, text):
        for line in text.splitlines():
            for segment in wrap(line, 80):
                self.write_line(segment)
            self.write_line("")

    def list_pages(self):
        pages = []
        for page in Page.objects.filter(published=True):
            pages.append((page.title, f"page:{page.pk}"))

        cfp = event.get_active_cfp()
        if cfp:
            pages.append((cfp.title, "cfp"))

        return sorted(pages)

    def pages_menu(self):
        for title, id in self.list_pages():
            self.file_item(title, id)

    def talks_menu(self):
        for talk in event.talks.prefetch_related('applicants__user'):
            title = f"{talk.title} - {talk.speaker_names}"
            self.file_item(title, f"talk:{talk.pk}")

    def workshops_menu(self):
        workshops = (event.workshops
            .prefetch_related('applicants__user')
            .filter(published=True)
            .order_by('title'))

        for workshop in workshops:
            speakers = ", ".join(workshop.applicant_names())
            title = f"{workshop.title} - {speakers}"
            self.file_item(title, f"workshop:{workshop.pk}")

    def news_menu(self):
        for post in event.posts.all():
            title = f"[{post.created_at.date()}] {post.title}"
            self.file_item(title, f"post:{post.pk}")

    def page(self, page_id):
        page = Page.objects.get(pk=page_id)
        markdown = render_to_string('pages/page.md', {"page": page})
        for line in markdown.splitlines():
            self.write_line(line)

    def talk(self, talk_id):
        talk = Talk.objects.get(pk=talk_id)
        markdown = render_to_string('talks/talk.md', {"talk": talk})
        for line in markdown.splitlines():
            self.write_line(line)

    def post(self, post_id):
        post = Post.objects.get(pk=post_id)
        markdown = render_to_string('blog/post.md', {"post": post})
        for line in markdown.splitlines():
            self.write_line(line)

    def workshop(self, workshop_id):
        workshop = Workshop.objects.get(pk=workshop_id)
        markdown = render_to_string('workshops/workshop.md', {"workshop": workshop})
        for line in markdown.splitlines():
            self.write_line(line)

    def cfp(self):
        cfp = event.get_active_cfp()
        if cfp:
            self.write_text(cfp.announcement)
        else:
            self.write_line("No active calls for paper.")

    def main_menu(self):
        has_workshops = event.workshops.filter(published=True).exists()
        has_talks = event.talks.exists()
        has_news = event.posts.exists()

        self.menu_item("Pages", "pages")
        if has_news:
            self.menu_item("News", "news")
        if has_talks:
            self.menu_item("Talks", "talks")
        if has_workshops:
            self.menu_item("Workshops", "workshops")

    def connectionMade(self):
        client_ip, client_port = self.transport.client
        print(f"Connection made from {client_ip}:{client_port}")

    def connectionLost(self, reason):
        client_ip, client_port = self.transport.client
        print(f"Connection lost from {client_ip}:{client_port}")

    def dataReceived(self, data):
        print("Received:", data)
        data = data.decode()

        if data == '\r\n':
            self.main_menu()
        elif data == 'pages\r\n':
            self.pages_menu()
        elif data == 'talks\r\n':
            self.talks_menu()
        elif data == 'news\r\n':
            self.news_menu()
        elif data == 'workshops\r\n':
            self.workshops_menu()
        elif re.match(r"^page:(\d+)\r\n$", data):
            self.page(int(data.split(":")[1]))
        elif re.match(r"^talk:(\d+)\r\n$", data):
            self.talk(int(data.split(":")[1]))
        elif re.match(r"^post:(\d+)\r\n$", data):
            self.post(int(data.split(":")[1]))
        elif re.match(r"^workshop:(\d+)\r\n$", data):
            self.workshop(int(data.split(":")[1]))
        elif data == 'cfp\r\n':
            self.cfp()
        else:
            print("???")

        self.transport.loseConnection()


class GopherFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Gopher()
