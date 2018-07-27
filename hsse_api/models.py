from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

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
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'password']

    def __str__(self):
        """String representation of the model"""

        return self.email
