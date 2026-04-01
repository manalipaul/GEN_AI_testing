from django.contrib import admin
from .models import Profile, Team, Activity, WorkoutSuggestion, Leaderboard, Workout

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('team', 'points', 'updated_at')
    search_fields = ('team__name',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'height_cm', 'weight_kg')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    filter_horizontal = ('members',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'duration_minutes', 'calories_burned', 'timestamp')
    list_filter = ('type', 'timestamp')


@admin.register(WorkoutSuggestion)
class WorkoutSuggestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'created_at')
    search_fields = ('title', 'description')
