from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Activity, Profile, Team, WorkoutSuggestion, Leaderboard, Workout
from .serializers import (
    ActivitySerializer,
    ProfileSerializer,
    TeamSerializer,
    UserSerializer,
    WorkoutSuggestionSerializer,
    LeaderboardSerializer,
    WorkoutSerializer,
)

class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class LeaderboardViewSet(viewsets.ModelViewSet):
    queryset = Leaderboard.objects.select_related('team').all()
    serializer_class = LeaderboardSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.prefetch_related('members').all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        team = serializer.save(owner=self.request.user)
        team.members.add(self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def join(self, request, pk=None):
        team = self.get_object()
        team.members.add(request.user)
        return Response({'status': 'joined'}, status=status.HTTP_200_OK)


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.select_related('user', 'team').all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkoutSuggestionViewSet(viewsets.ModelViewSet):
    queryset = WorkoutSuggestion.objects.all()
    serializer_class = WorkoutSuggestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class LeaderboardAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def get_queryset(self):
        users = User.objects.annotate(total_calories=Sum('activities__calories_burned')).order_by('-total_calories')
        return users

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()[:10]
        data = [
            {
                'username': user.username,
                'total_calories': user.total_calories or 0,
                'total_activities': user.activities.count(),
            }
            for user in queryset
        ]
        return Response(data)


class SuggestionAPIView(generics.ListAPIView):
    queryset = WorkoutSuggestion.objects.all()
    serializer_class = WorkoutSuggestionSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        level = request.GET.get('difficulty', 'medium')
        queryset = self.get_queryset().filter(difficulty__iexact=level)
        if not queryset.exists():
            queryset = self.get_queryset()[:5]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

