from django.db import models
from django.contrib.auth.models import AbstractUser


class Stacks(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=30)

    def __str__(self):
        return self.tag


class User(AbstractUser):
    GENDER_CHOICES = {
        "M": "Male",
        "F": "Female",
        "O": "Other",
    }
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, blank=True, null=True, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    online_status = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    urls = models.JSONField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    mentors = models.ManyToManyField('Mentor', symmetrical=False, default=None, related_name='my_mentors')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    learning_stacks = models.ManyToManyField(Stacks, default=None)

    def __str__(self):
        return self.username if self.username else self.email


class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    description = models.TextField()
    rating = models.FloatField(null=True, blank=True)
    is_available = models.BooleanField(default=False)
    history = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stacks = models.ManyToManyField(Stacks)

    def __str__(self):
        return self.user.username if self.user.username else self.user.email


class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.TextField()
    rating = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_commenting')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_commented')
    stacks = models.ManyToManyField(Stacks)

    def __str__(self):
        return f"Comment by {self.from_user.email} to {self.to_user.email}"


class Requests(models.Model):
    STATUS_CHOICES = {
        "P": "Pending",
        "A": "Accepted",
        "R": "Rejected",
    }
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_requesting')
    to_mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentor_requested')
    stacks = models.ManyToManyField(Stacks)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Request from {self.from_user.email} to {self.to_mentor.email}"
