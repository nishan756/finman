
from dotenv import load_dotenv
load_dotenv()
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()
class Command(BaseCommand):
    help = 'Creates a superuser.'

    def handle(self, *args, **options):
        if not User.objects.filter(username=os.getenv('DJANGO_SUPERUSER_USERNAME')).exists():
            User.objects.create_superuser(
                username=os.getenv('DJANGO_SUPERUSER_USERNAME'),
                email=os.getenv('DJANGO_SUPERUSER_EMAIL'),
                password=os.getenv('DJANGO_SUPERUSER_PASSWORD'),
            )
        print('Superuser has been created.')