from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DomainViewSet, DisciplineViewSet, TrackViewSet, LevelViewSet, CourseViewSet,
    ChapterViewSet, ContentViewSet, ReviewViewSet, FavouriteViewSet,
    TrackEnrollmentViewSet, CourseProgressViewSet, CourseDetailBySlug
)

router = DefaultRouter()
router.register(r'domains', DomainViewSet)
router.register(r'disciplines', DisciplineViewSet)
router.register(r'tracks', TrackViewSet)
router.register(r'levels', LevelViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'chapters', ChapterViewSet)
router.register(r'contents', ContentViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'favourites', FavouriteViewSet)
router.register(r'enrollments', TrackEnrollmentViewSet)
router.register(r'progress', CourseProgressViewSet)

urlpatterns = [
    path('courses/<slug:slug>/', CourseDetailBySlug.as_view(), name='course-detail-slug'),
    path('', include(router.urls)),
]
