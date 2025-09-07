from rest_framework import serializers
from .models import (
    Domain, Discipline, Track, Level, Course,
    Chapter, Content, Review, Favourite,
    TrackEnrollment, CourseProgress
)


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = "__all__"


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = "__all__"


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = "__all__"


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = "__all__"


# Nested serializers
class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ["id", "title", "type", "order", "data"]

class ChapterSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, read_only=True)
    subchapters = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = ["id", "title", "description", "order", "subchapters", "contents"]

    def get_subchapters(self, obj):
        children = obj.get_children()
        return ChapterSerializer(children, many=True).data

class CourseSerializer(serializers.ModelSerializer):
    domain = DomainSerializer(read_only=True)
    discipline = DisciplineSerializer(read_only=True)
    track = TrackSerializer(read_only=True)
    level = LevelSerializer(read_only=True)
    class Meta:
        model = Course
        fields = "__all__"

class CourseDetailSerializer(serializers.ModelSerializer):
    domain = DomainSerializer(read_only=True)
    discipline = DisciplineSerializer(read_only=True)
    track = TrackSerializer(read_only=True)
    level = LevelSerializer(read_only=True)
    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            "id", "title", "slug", "about", "description", "teacher", 
            "price", "price_unit", "language", "status", "published_at", 
            "thumbnail", "domain", "discipline", "track", "level", "chapters"
        ]





class ReviewSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.username", read_only=True)

    class Meta:
        model = Review
        fields = "__all__"


class FavouriteSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.username", read_only=True)

    class Meta:
        model = Favourite
        fields = "__all__"


class TrackEnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.username", read_only=True)
    track_name = serializers.CharField(source="track.name", read_only=True)

    class Meta:
        model = TrackEnrollment
        fields = "__all__"


class CourseProgressSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.username", read_only=True)
    course_title = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = CourseProgress
        fields = "__all__"
