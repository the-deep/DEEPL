import os
from importlib import import_module

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Scripts runner which uses django context"

    def add_arguments(self, parser):
        parser.add_argument('scriptname', type=str)
        parser.add_argument('extra', nargs='*', type=str, default=[])

    def handle(self, *args, **options):
        scriptname = options['scriptname']
        other_args = options['extra']
        basedir = './'
        # list dirs and filter only directories
        apps = list(filter(
            lambda x: (x[0] not in '._=' and
                    os.path.isdir(os.path.join(basedir, x))),
            os.listdir(basedir)))
        try:
            script = import_module('scripts.{}'.format(scriptname))
        except ImportError:
            # check in other apps
            for app in apps:
                try:
                    toimport = '{}.scripts.{}'.format(
                        app, scriptname
                    )
                    script = import_module(toimport)
                except ImportError:
                    pass
                else:
                    return script.main(*other_args)
            else:
                print("ERROR!! The script you requesed does not exist.")
                return
        else:
            return script.main(*other_args)
        # the script should have main function accepting *args
