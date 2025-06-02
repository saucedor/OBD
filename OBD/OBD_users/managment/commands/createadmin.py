from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Creates a default admin user"

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="LeadlyAdmin",
                email="leadly@prime.com",
                password="fjbgrhuirhfiuawh8900"
            )
            self.stdout.write(self.style.SUCCESS("✔ Superuser 'LeadlyAdmin' creado"))
        else:
            self.stdout.write(self.style.WARNING("⚠ El superuser ya existe"))
