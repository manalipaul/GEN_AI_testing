from django.test import TestCase
from django.contrib.auth.models import User
from .models import Team, Workout, Leaderboard

class WorkoutModelTest(TestCase):
	def test_create_workout(self):
		workout = Workout.objects.create(name='Test Workout', description='A test workout')
		self.assertEqual(str(workout), 'Test Workout')

class LeaderboardModelTest(TestCase):
	def test_create_leaderboard(self):
		user = User.objects.create(username='testuser')
		team = Team.objects.create(name='Test Team', owner=user)
		leaderboard = Leaderboard.objects.create(team=team, points=50)
		self.assertIn('Test Team', str(leaderboard))
