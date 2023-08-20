from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Adds test users for testing purposes'

    def handle(self, *args, **options):
        # Add your code to create test users here
        user1 = User.objects.create_user(username="alice", password="redqueen")
        user2 = User.objects.create_user(username="bob", password="squarepants")

        self.stdout.write(self.style.SUCCESS('Test users added successfully'))