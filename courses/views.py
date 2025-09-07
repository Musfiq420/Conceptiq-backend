from rest_framework import viewsets, permissions
from .models import (
    Domain, Discipline, Track, Level, Course,
    Chapter, Content, Review, Favourite,
    TrackEnrollment, CourseProgress
)
from .serializers import (
    DomainSerializer, DisciplineSerializer, TrackSerializer, LevelSerializer, CourseSerializer,
    ChapterSerializer, ContentSerializer, ReviewSerializer, FavouriteSerializer,
    TrackEnrollmentSerializer, CourseProgressSerializer, CourseDetailSerializer
)

from rest_framework.generics import RetrieveAPIView

class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    permission_classes = [permissions.AllowAny]


class DisciplineViewSet(viewsets.ModelViewSet):
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer
    permission_classes = [permissions.AllowAny]


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [permissions.AllowAny]


class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    permission_classes = [permissions.AllowAny]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]

class CourseDetailBySlug(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    lookup_field = 'slug'


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [permissions.AllowAny]


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [permissions.AllowAny]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]


class FavouriteViewSet(viewsets.ModelViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer
    permission_classes = [permissions.AllowAny]


class TrackEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = TrackEnrollment.objects.all()
    serializer_class = TrackEnrollmentSerializer
    permission_classes = [permissions.AllowAny]


class CourseProgressViewSet(viewsets.ModelViewSet):
    queryset = CourseProgress.objects.all()
    serializer_class = CourseProgressSerializer
    permission_classes = [permissions.AllowAny]
