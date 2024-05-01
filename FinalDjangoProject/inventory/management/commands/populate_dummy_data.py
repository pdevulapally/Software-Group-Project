from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from inventory.models import Equipment, Booking
from datetime import timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populates the database with multiple dummy equipment and bookings'

    def handle(self, *args, **options):
        # Create a dummy user if not already present
        if not User.objects.filter(username='testuser').exists():
            user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
        else:
            user = User.objects.get(username='testuser')

        # Equipment details
        equipment_names = ['HP Pavilion', 'Dell XPS', 'Samsung Monitor', 'Apple iPad']
        categories = ['Laptop', 'Desktop', 'Monitor', 'Tablet']
        cpus = ['Intel i7', 'AMD Ryzen 7', 'Intel i5', 'Apple M1']

        # Generate multiple equipment items
        for i in range(1, 21):  # Generating 20 items
            equipment, created = Equipment.objects.update_or_create(
                serial_number=f'Serial{i}',  # Assuming the 'device_serial' field name is now 'serial_number'
                defaults={
                    'name': equipment_names[i % len(equipment_names)],
                    'category': categories[i % len(categories)],
                    'cpu': cpus[i % len(cpus)],
                    'status': 'Available'  # Ensuring all are set to Available
                }
            )

            # Create associated bookings for every second available equipment
            if i % 2 == 0 and created:
                Booking.objects.create(
                    start_date=timezone.now(),
                    end_date=timezone.now() + timedelta(days=i),
                    approval_status=True,
                    user=user,
                    equipment=equipment
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy equipment and bookings.'))
