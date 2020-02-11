from django.core.management.base import BaseCommand

from wordy_game_app.models import *


class Command(BaseCommand):
    help = 'Creates a superuser and a WordyUser account for that superuser'

    def handle(self, *args, **kwargs):
        # If necessary, delete existing account with name 'matt'
        # Create a WordyUser that is a superuser

        my_account = WordyUser(
            username='matt',
            email='matt@mattkennett.com',
            favorite_color='blue',
        )
        my_account.save()

        my_account.set_password('abc123')
        my_account.save()
