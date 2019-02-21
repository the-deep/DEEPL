import os
from importlib import import_module

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Scripts runner which uses django context"

    def add_arguments(self, parser):
        parser.add_argument('scriptname', type=str)
        # parser.add_argument('extra', nargs='*', type=str, default=[])
        parser.add_argument(
            '--model_version', type=str, default=None,
            help="Version of model(if creating one)"
        )
        parser.add_argument(
            '--model_name', type=str, default=None,
            help="Name of model(if creating one)")
        parser.add_argument(
            '--num_clusters', type=str, default=None,
            help="Name of model(if creating one)")
        parser.add_argument(
            '--class_name', type=str, default=None,
            help="Name of model class")
        parser.add_argument(
            '--plot_type', type=str, default=None,
            help="2d or 3d plot")
        parser.add_argument(
            '--cluster_method', type=str, default=None,
            help="Clustering method: doc2vec or bow(normal)")
        parser.add_argument(
            '--doc2vec_group_id', type=str, default=None,
            help="GroupId of Doc2VecModel. Used with clustering method doc2vec"
        )
        parser.add_argument(
            '--group_id', type=str, default=None,
            help="Group id of Model."
        )
        parser.add_argument(
            '--path', type=str, default=None,
            help='Path of some file'
        )
        parser.add_argument(
            '--type', type=str, default=None,
            help='Type of classifier model'
        )
        parser.add_argument(
            '--dictionary_path', type=str, default=None,
            help='Path of dictionary'
        )
        parser.add_argument(
            '--model_path', type=str, default=None,
            help='Path of model pickle'
        )
        parser.add_argument(
            '--pca_model_path', type=str, default=None,
            help='Path of some pca model pickle'
        )
        parser.add_argument(
            '--tfidf_model_path', type=str, default=None,
            help='Path of tfidf model pickle'
        )
        # Add other custom args required by the scripts

    def handle(self, *args, **options):
        scriptname = options.pop('scriptname')
        basedir = './'
        other_kwargs = options
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
                except ImportError as e:
                    pass
                else:
                    return script.main(**other_kwargs)
            else:
                print("ERROR!! The script you requesed does not exist.")
                return
        else:
            return script.main(**other_kwargs)
        # the script should have main function accepting *args and **kwargs
