from django.urls import include, path
from rest_framework import routers

from .views import (
    ActivityViewSet,
    LeaderboardAPIView,
    ProfileViewSet,
    SuggestionAPIView,
    TeamViewSet,
    UserViewSet,
    WorkoutSuggestionViewSet,
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'suggestions', WorkoutSuggestionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('leaderboard/', LeaderboardAPIView.as_view(), name='leaderboard'),
    path('recommendations/', SuggestionAPIView.as_view(), name='recommendations'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
