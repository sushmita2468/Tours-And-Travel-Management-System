

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(email, username, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)  # This field is for the hashed password
    profile_picture = models.ImageField(upload_to='profile_images/')
    bio = models.TextField()
    contact_info = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('guide', 'Guide'),
        ('hotel_manager', 'Hotel Manager'),
        ('cab_rental', 'Cab Rental'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # Add other fields as needed

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Specify the email field as the username for authentication
    REQUIRED_FIELDS = ['username']

    # Specify custom related names to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_profiles',  # Custom related name
        blank=True,
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_profiles',  # Custom related name
        blank=True,
    )

    def set_password(self, raw_password):
        # Hash the provided raw password and store it in the 'password' field.
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        # Check if the provided raw password matches the hashed password in the 'password' field.
        return check_password(raw_password, self.password)



class Destinations(models.Model):
    destination_id = models.AutoField(primary_key=True)
    destination_name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='destination_images/')

class Trips(models.Model):
    trip_id = models.AutoField(primary_key=True)
    trip_name = models.CharField(max_length=255)
    destination = models.ForeignKey(Destinations, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    organizer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    description = models.TextField()
    max_participants = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class TripDetails(models.Model):
    participant_id = models.AutoField(primary_key=True)
    trip = models.ForeignKey(Trips, on_delete=models.CASCADE)
    organizer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel_provider_id = models.CharField(max_length=255, null=True, blank=True)
    cab_rental_provider_id = models.CharField(max_length=255, null=True, blank=True)
    guide_provider_id = models.CharField(max_length=255, null=True, blank=True)

class HotelProviders(models.Model):
    provider_id = models.AutoField(primary_key=True)
    provider_name = models.CharField(max_length=255)
    description = models.TextField()
    contact_info = models.CharField(max_length=255)
    services_offered = models.TextField()
    ratings = models.DecimalField(max_digits=3, decimal_places=2)
    images = models.ImageField(upload_to='provider_images/')

class CabRentalProviders(models.Model):
    provider_id = models.AutoField(primary_key=True)
    provider_name = models.CharField(max_length=255)
    description = models.TextField()
    contact_info = models.CharField(max_length=255)
    services_offered = models.TextField()
    ratings = models.DecimalField(max_digits=3, decimal_places=2)
    images = models.ImageField(upload_to='provider_images/')

class GuideProviders(models.Model):
    provider_id = models.AutoField(primary_key=True)
    provider_name = models.CharField(max_length=255)
    description = models.TextField()
    contact_info = models.CharField(max_length=255)
    services_offered = models.TextField()
    ratings = models.DecimalField(max_digits=3, decimal_places=2)
    images = models.ImageField(upload_to='provider_images/')

class TripRatings(models.Model):
    trip = models.ForeignKey(Trips, on_delete=models.CASCADE)
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel_rating = models.IntegerField()
    cab_rental_rating = models.IntegerField()
    guide_rating = models.CharField(max_length=255)

