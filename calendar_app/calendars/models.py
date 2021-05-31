from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address!')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser):

    email = models.EmailField(
        verbose_name='email address',
        max_length=100,
        unique=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'login'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, unique=False)
    last_name = models.CharField(max_length=50, unique=False)
    address = models.CharField(max_length=50)

    class Meta:
        db_table = "profile"


class Event(models.Model):
    name = models.CharField
    date = models.DateField
    description = models.TextField

    def __str__(self):
        return self.name


class Date(models.Model):
    date = models.DateField
    event = models.ManyToManyField(Event)
    summary = models.CharField

    def __str__(self):
        return self.date


class Calendar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dates = models.ManyToManyField(Date)

    def __str__(self):
        return self.user
