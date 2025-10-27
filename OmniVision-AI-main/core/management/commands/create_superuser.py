from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser if it does not exist'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='admin', help='Username for superuser')
        parser.add_argument('--password', default='admin123', help='Password for superuser')
        parser.add_argument('--email', default='admin@omnivision.ai', help='Email for superuser')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']

        try:
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'Superuser "{username}" already exists.')
                )
            else:
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created superuser "{username}"')
                )
        except IntegrityError:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser "{username}"')
            )
