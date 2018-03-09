from django.core.management.base import BaseCommand
from importlib import import_module


class Command(BaseCommand):

    help = "Scripts runner which uses django context"

    def add_arguments(self, parser):
        parser.add_argument('scriptname', type=str)
        parser.add_argument('extra', nargs='*', type=str, default=[])

    def handle(self, *args, **options):
        scriptname = options['scriptname']
        other_args = options['extra']
        try:
            script = import_module('scripts.{}'.format(scriptname))
        except ModuleNotFoundError:
            print("ERROR!! The script you requesed does not exist.")
            return
        # the script should have main function accepting *args
        return script.main(*other_args)
