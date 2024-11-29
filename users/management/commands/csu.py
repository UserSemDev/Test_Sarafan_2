import os
from django.core.management import BaseCommand
from dotenv import load_dotenv
from config.settings import BASE_DIR
from users.models import User


class Command(BaseCommand):
    """Создание суперпользователя"""

    def handle(self, *args, **options):
        dotenv_path = os.path.join(BASE_DIR, '.env')
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
        user = User.objects.create(
            name='admin',
            email=os.getenv('ADMIN_EMAIL'),
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        user.set_password(os.getenv('ADMIN_PASSWORD'))
        user.save()
