import subprocess
import re

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Command to list available scripts to be run by command 'runscript'"

    def add_arguments(self, parser):
        # nothing to do here
        pass

    def handle(self, *args, **options):
        script = [
            'find', '-type', 'd', '-name',
            'scripts', '-exec', 'ls', '{}', ';'
        ]
        p = subprocess.Popen(script, stdout=subprocess.PIPE)
        o, e = p.communicate()
        files = o.split()
        scriptnames = []
        for f in files:
            fstr = f.decode()  # f is bytes
            if re.search('^__', fstr):
                continue
            if not re.search('\.py$', fstr):
                continue
            scriptnames.append(re.sub('\.py$', '', fstr))
        if not scriptnames:
            print("-- NO scripts available --")
            return
        print('========================')
        print(' The scripts available:')
        print('========================')
        for name in scriptnames:
            print('-', name)
