from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.full_name


class Beneficiary(models.Model):
    manager = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=55)
    email = models.EmailField()
    name = models.CharField(max_length=80)
    cell = models.CharField(max_length=25)
    address = models.CharField(max_length=800)
    about = models.TextField()
    city = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='logos', blank=True, null=True)
    cover_image = models.ImageField(upload_to='covers', blank=True, null=True)
    latitude = models.DecimalField(decimal_places=5, null=True, max_digits=10)
    longitude = models.DecimalField(decimal_places=5, null=True, max_digits=10)
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class OnlineDonation(models.Model):
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=50)
    currency = models.CharField(max_length=55)
    payment_method = models.CharField(max_length=55)
    donor_name = models.CharField(default='Anonymous', max_length=55)
    donor_email = models.EmailField(null=True)
    donor_cell = models.CharField(max_length=55, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.beneficiary.name
