from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email
