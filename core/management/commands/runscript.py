from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Scripts runner which uses django context"

    def add_arguments(self, parser):
        parser.add_argument('script', nargs='+', type=str)

    def handle(self, *args, **options):
        scriptname = options['script'][0]
        if scriptname == 'confidence_graph':
            self.confidence_graph()
        else:
            print('NO SUCH SCRIPT FOUND.')

    def confidence_graph(self):
        from scripts.confidence_graph import main
        main()
