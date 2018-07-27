from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class UserManager(BaseUserManager):
    """Manager For User Creation"""

    def create(self, email, name, password):
        """Yup, what it says"""
        if not email:
            raise ValueError("Hey! We need an email")
        email = self.normalize_email(email)
        user = self.model(name=name, email=email)
        user.set_password(password)
        user.save(using=self._db)

        return user

class User(AbstractBaseUser):
    """Represents a 'user profile' inside our system"""

    email = models.EmailField(max_length=255, blank=False, unique=True)
    name = models.CharField(max_length=255, blank=False)
    # last_login = models.DateField(auto_now=True)
    objects = UserManager()
    # token = models.CharField(max_length=255)
    USERNAME_FIELD = 'email' # What we are going to use for login
    REQUIRED_FIELDS = ['name', 'password']

    def __str__(self):
        """String representation of the model"""

        return self.email
