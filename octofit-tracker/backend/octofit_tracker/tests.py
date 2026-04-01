from django.test import TestCase
from .models import User, Team, Workout, Activity, Leaderboard
from django.utils import timezone

class ModelTests(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Marvel', description='Marvel superheroes')
        self.user = User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=self.team)
        self.workout = Workout.objects.create(name='Web Swing', description='Swinging through the city')
        self.activity = Activity.objects.create(user=self.user, workout=self.workout, date=timezone.now(), duration=30)
        self.leaderboard = Leaderboard.objects.create(user=self.user, score=100)

    def test_user_team(self):
        self.assertEqual(self.user.team.name, 'Marvel')

    def test_activity_workout(self):
        self.assertEqual(self.activity.workout.name, 'Web Swing')

    def test_leaderboard_score(self):
        self.assertEqual(self.leaderboard.score, 100)
