from django.core.management.base import BaseCommand
from twisted.internet import reactor, endpoints
from gopher.protocol import GopherFactory


class Command(BaseCommand):
    help = "Start the gopher server"

    def add_arguments(self, parser):
        parser.add_argument("port", default="70", type=int, nargs="?")

    def handle(self, *args, **options):
        port = options.get("port")
        server = endpoints.serverFromString(reactor, f"tcp:{port}")
        server.listen(GopherFactory())
        print(f"Listening on port {port}...")
        reactor.run()
