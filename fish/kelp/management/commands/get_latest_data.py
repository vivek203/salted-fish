from django.core.management.base import BaseCommand, CommandError
import time
# from kelp.models import 

class Command(BaseCommand):
    help = 'gets latest data from remote servers and udates our db'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        while(True):
            self.stdout.write('TEST')
            time.sleep(5)