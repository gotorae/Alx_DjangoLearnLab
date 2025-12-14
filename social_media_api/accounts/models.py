# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from django.utils import timezone

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The email address must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)  # <-- correct kwarg
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    # Keep username field (AbstractUser requires it), but we will log in with email
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to="profile_photos/", null=True, blank=True)
    # Directed follow: A can follow B without B auto-following A
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following", blank=True
    )
    

    objects = CustomUserManager()

    USERNAME_FIELD = "email"           # primary identifier
    REQUIRED_FIELDS = ["username"]     # still collect a username for admin



    def __str__(self):
            return self.email


