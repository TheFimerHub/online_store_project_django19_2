from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Create a superuser with specified email and password'

    def handle(self, *args, **kwargs):
        email = 'admin@st.shop'
        first_name = 'Admin'
        last_name = 'Stepanoff'
        password = 'stepanoff'

        user = User.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_superuser=True
        )
        user.set_password(password)
        user.save()

        self.stdout.write(self.style.SUCCESS(f'Superuser "{email}" has been successfully created.'))
