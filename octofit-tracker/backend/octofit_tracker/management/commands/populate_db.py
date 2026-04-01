from django.core.management.base import BaseCommand
from octofit_tracker.models import Team, Activity, Leaderboard, Workout, User

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete existing data
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        Team.objects.all().delete()
        User.objects.all().delete()

        # Create Teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create Users (superheroes)
        users = [
            User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
            User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel),
            User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
            User.objects.create(name='Batman', email='batman@dc.com', team=dc),
        ]

        # Create Activities
        activities = [
            Activity.objects.create(user=users[0], type='Running', duration=30),
            Activity.objects.create(user=users[1], type='Cycling', duration=45),
            Activity.objects.create(user=users[2], type='Swimming', duration=60),
            Activity.objects.create(user=users[3], type='Yoga', duration=40),
        ]

        # Create Workouts
        workouts = [
            Workout.objects.create(name='Morning Cardio', description='Cardio for all'),
            Workout.objects.create(name='Strength Training', description='Strength for heroes'),
        ]

        # Create Leaderboard
        Leaderboard.objects.create(team=marvel, points=100)
        Leaderboard.objects.create(team=dc, points=90)

        self.stdout.write(self.style.SUCCESS('Test data populated successfully.'))
