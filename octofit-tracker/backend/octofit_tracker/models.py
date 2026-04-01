
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Workout(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Leaderboard(models.Model):
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='leaderboards')
    points = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.team.name} - {self.points} points"


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    height_cm = models.PositiveIntegerField(null=True, blank=True)
    weight_kg = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class Team(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owned_teams', on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='teams', blank=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('run', 'Running'),
        ('cycle', 'Cycling'),
        ('swim', 'Swimming'),
        ('strength', 'Strength Training'),
        ('yoga', 'Yoga'),
        ('hike', 'Hiking'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities')
    type = models.CharField(max_length=30, choices=ACTIVITY_TYPES)
    duration_minutes = models.PositiveIntegerField()
    distance_km = models.FloatField(null=True, blank=True)
    calories_burned = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.get_type_display()} - {self.timestamp.date()}"


class WorkoutSuggestion(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    difficulty = models.CharField(max_length=30, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')])
    target_muscles = models.CharField(max_length=180, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

