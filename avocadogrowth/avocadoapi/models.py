"""
Models for the Avocado API
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager

AUTH_USER_MODEL = settings.AUTH_USER_MODEL


class UserManager(BaseUserManager):
    def create_user(self, **kwargs):
        # pylint: disable=missing-function-docstring
        if "email" not in kwargs:
            raise ValueError("Email is required")
        if "password" not in kwargs:
            raise ValueError("Password is required")
        user = self.model(
            email=self.normalize_email(kwargs["email"]),
        )
        user.set_password(kwargs["password"])
        kwargs.pop("password")
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        # pylint: disable=missing-function-docstring
        # pylint: disable=missing-function-docstring
        user = self.create_user(**kwargs)
        user.is_admin = True
        user.save(using=self._db)
        return user


class Stacks(models.Model):
    """
    Model for Stacks
    """
    id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.tag


class User(AbstractUser):
    """
    Custom User model for Avocado API
    """
    GENDER_CHOICES = {
        "M": "Male",
        "F": "Female",
        "O": "Other",
    }
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, blank=True, null=True, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    online_status = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    urls = models.JSONField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    mentors = models.ManyToManyField("Mentor", symmetrical=False, default=None, related_name="my_mentors")
    updated_at = models.DateTimeField(auto_now=True)
    learning_stacks = models.ManyToManyField(Stacks, default=None)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def is_mentor(self):
        # pylint: disable=missing-function-docstring
        return Mentor.objects.filter(user=self).exists()

    def get_requests(self):
        # pylint: disable=missing-function-docstring
        return Requests.objects.filter(from_user=self)

    def get_stacks(self):
        # pylint: disable=missing-function-docstring
        return self.learning_stacks.all()

    def __str__(self):
        return self.username if self.username else self.email


class Mentor(models.Model):
    """
    Model for Mentor
    """
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    description = models.TextField()
    rating = models.FloatField(null=True, blank=True)
    is_available = models.BooleanField(default=False)
    history = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stacks = models.ManyToManyField(Stacks)

    def get_comments(self):
        # pylint: disable=missing-function-docstring
        return Comments.objects.filter(to_user=self)

    def get_requests(self):
        # pylint: disable=missing-function-docstring
        return Requests.objects.filter(to_mentor=self)

    def get_stacks(self):
        # pylint: disable=missing-function-docstring
        return self.stacks.all()

    def __str__(self):
        return self.user.username if self.user.username else self.user.email


class Comments(models.Model):
    """
    Model for Comments
    """
    id = models.AutoField(primary_key=True)
    comment = models.TextField()
    rating = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    from_user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_commenting")
    to_user = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name="mentor_commented")
    stacks = models.ManyToManyField(Stacks)

    def __str__(self):
        return f"Comment by {self.from_user.email} to {self.to_user.email}"


class Requests(models.Model):
    """
    Model for Requests
    """
    STATUS_CHOICES = {
        "P": "Pending",
        "A": "Accepted",
        "R": "Rejected",
    }
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    from_user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_requesting")
    to_mentor = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mentor_requested")
    stacks = models.ManyToManyField(Stacks)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Request from {self.from_user.email} to {self.to_mentor.email}"
