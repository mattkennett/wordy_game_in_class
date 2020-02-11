from django.core.management.base import BaseCommand

from wordy_game_app.models import *
from wordy_game_app.views import *


class Command(BaseCommand):
    help = 'Just a quick way to run a random command if necessary'

    def handle(self, *args, **kwargs):
        print('Hello World!')
