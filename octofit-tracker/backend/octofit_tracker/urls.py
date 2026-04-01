from django.urls import include, path
from rest_framework import routers

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .views import (
    ActivityViewSet,
    LeaderboardViewSet,
    ProfileViewSet,
    TeamViewSet,
    UserViewSet,
    WorkoutSuggestionViewSet,
    WorkoutViewSet,
)


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'workouts', WorkoutViewSet)
router.register(r'leaderboards', LeaderboardViewSet)
router.register(r'suggestions', WorkoutSuggestionViewSet)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'profiles': reverse('profile-list', request=request, format=format),
        'teams': reverse('team-list', request=request, format=format),
        'activities': reverse('activity-list', request=request, format=format),
        'workouts': reverse('workout-list', request=request, format=format),
        'leaderboards': reverse('leaderboard-list', request=request, format=format),
        'suggestions': reverse('workoutsuggestion-list', request=request, format=format),
    })

urlpatterns = [
    path('', api_root, name='api-root'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
