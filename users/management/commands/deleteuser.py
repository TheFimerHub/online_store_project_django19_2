from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Deletes a user by id'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='The ID of the user to delete')

    def handle(self, *args, **kwargs):
        user_id = kwargs['user_id']
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            self.stdout.write(self.style.SUCCESS(f'User with id {user_id} has been successfully deleted.'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User with id {user_id} does not exist.'))
