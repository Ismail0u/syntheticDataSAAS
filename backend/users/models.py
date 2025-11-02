from django.contrib.auth.models import AbstractUser
from django.db import models


# --- CUSTOM USER MODEL ---
class User(AbstractUser):
    """
    Custom User model extending Django's built-in AbstractUser.
    
    It includes fields necessary for subscription plans and daily quota tracking, 
    which are essential for the SAAS business logic.
    """
    
    # Choices for the user's subscription plan (quota limits are enforced based on this)
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    ]
    
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    # Overrides the default username field with email, ensuring uniqueness.
    email = models.EmailField(unique=True)

    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    daily_quota_used = models.IntegerField(default=0)

    # Stores the date when the daily quota was last reset. Used to check for new days.
    # auto_now_add=True sets the date on creation. It's updated programmatically in views.py.
    last_quota_reset = models.DateField(auto_now_add=True)
    
    # Tells Django to use the 'email' field as the unique identifier for login.
    USERNAME_FIELD = 'email'
    
    # Fields required when creating a user via the createsuperuser management command (excluding password and USERNAME_FIELD).
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email