from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from authentication.serializers import UserSerializer
from authentication.models import UserData


super_users = [
    {
    'username': 'william',
    'email': 'williamsebastiani.97@gmail.com',
    'password': 'midnight'
    },
    {
    'username': 'pietro',
    'email': 'pietrociattaglia@gmail.com',
    'password': 'midnight'
    },
]


class Command(BaseCommand):
    help = 'Init DB'

    # def add_arguments(self, parser):
    #     parser.add_argument('number', nargs='+', type=int)

    def handle(self, *args, **options):
        print('working')
        data = {
            'email': 'gino.b@mail.com',
            'password': 'bellapete',
            'first_name': 'gino',
            'last_name': 'b',
            'is_staff': True,
            'is_superuser': True,
            'is_active': True
        }
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = UserData.objects.get(email=data['email'])
        user.set_password('bellapete')
        # user.set_password('bellapete')