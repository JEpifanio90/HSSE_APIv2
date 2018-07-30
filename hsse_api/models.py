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

class Corrective_Action(models.Model):

    STATUS_CHOICES = (
        ("OV", "Overdue"),
        ("CL", "Closed"),
        ("IP", "In progress"),
        ("O", "Open")
    )
    action = models.CharField(max_length=120, blank=False)
    due_date = models.DateField(auto_now=False, auto_now_add=False)    
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default="O")
    supervisor = models.CharField(max_length=60)
    other_participants = models.CharField(max_length=60)
    ehhs = models.CharField(max_length=60)
    manager = models.CharField(max_length=60)


class User(AbstractBaseUser, models.Model):
    """Represents a 'user profile' inside our system"""

    email = models.EmailField(max_length=255, blank=False, unique=True)
    name = models.CharField(max_length=255, blank=False)
    corrective_action = models.ForeignKey(Corrective_Action, related_name="corrective_actions", on_delete=models.CASCADE, blank=True, null=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'password']

    def __str__(self):
        """String representation of the model"""

        return self.email

class Site(models.Model):
    """Represents a working site"""

    name = models.CharField(max_length=100, blank=False)
    address = models.CharField(max_length=255, blank=False)
    city = models.CharField(max_length=70, blank=False)
    state = models.CharField(max_length=50, blank=False)
    country = models.CharField(max_length=70, blank=False)
    user = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['name', 'city', 'state', 'country']

    def __str__(self):
        """String representation of our working site"""
        return self.name
