from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from inventory.models import Student

class Command(BaseCommand):
    help = 'Create new student users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number',
            default=10,
            type=int,
            help='Number of students to create',
        )

    def handle(self, *args, **options):
        number_of_students = options['number']
        base_username = "student"
        existing_users = User.objects.filter(username__startswith=base_username).count()
        start_index = existing_users + 1  # Start indexing after the last existing student

        for i in range(start_index, start_index + number_of_students):
            username = f'{base_username}{i}'
            email = f'{username}@example.com'

            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=email, password='password')
                Student.objects.create(user=user, grade='Grade 10', adminApprovalStatus=False)  # Ensure adminApprovalStatus is set to False
                self.stdout.write(self.style.SUCCESS(f'Successfully created user {username}'))
            else:
                self.stdout.write(self.style.WARNING(f'User {username} already exists.'))
