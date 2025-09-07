from django.db import models
from django.utils import timezone
from users.models import Profile
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models import JSONField
from django.utils.text import slugify

class Domain(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Discipline(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name="disciplines")
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('domain', 'name')

    def __str__(self):
        return f"{self.domain.name} → {self.name}"


class Track(models.Model):  # previously Path
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name="tracks")
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('domain', 'name')

    def __str__(self):
        return f"{self.domain.name} → {self.name}"


class Level(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"




class Course(models.Model):
    PRICE_UNITS = [
        ('bdt', 'BDT'),
        ('usd', 'USD'),
        ('eur', 'EUR'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)  # ✅ new field
    about = models.CharField(max_length=300, blank=True, null=True)  # short description
    description = models.TextField()
    teacher = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})

    # hierarchy relations
    domain = models.ForeignKey(Domain, on_delete=models.SET_NULL, null=True, related_name="courses")
    discipline = models.ForeignKey(Discipline, on_delete=models.SET_NULL, null=True, related_name="courses")
    track = models.ForeignKey(Track, on_delete=models.SET_NULL, null=True, related_name="courses")
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, related_name="courses")

    # business fields
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_unit = models.CharField(max_length=10, choices=PRICE_UNITS, default='bdt')
    language = models.CharField(max_length=100, default="English")

    # status
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    published_at = models.DateTimeField(blank=True, null=True)

    # metadata
    thumbnail = models.ImageField(upload_to="course_thumbnails/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            # ensure uniqueness
            while Course.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        if self.status == "published" and self.published_at is None:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.domain.name if self.domain else 'NoDomain'})"





# -------------------------------
# COURSE CONTENT MODELS (MPTT)
# -------------------------------

class Chapter(MPTTModel):
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="chapters")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='subchapters'
    )

    class MPTTMeta:
        order_insertion_by = ['order']

    class Meta:
        unique_together = ("course", "title")

    def __str__(self):
        return f"{self.course.title} → {self.title}"
    

class Content(models.Model):
    CONTENT_TYPES = [
        ('lesson', 'Lesson'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
    ]

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="contents")
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=CONTENT_TYPES, default='lesson')
    index = models.CharField(max_length=100, blank=True, null=True)  # e.g., "0|hzzzzz:"

    # Store the full data JSON (blocks, zones, root, etc.)
    data = JSONField(default=dict, blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.chapter.title} → {self.title}"

# -------------------------------
# USER BEHAVIOR MODELS
# -------------------------------

class Review(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(default=0)  # 1–5 scale
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "course")  # one review per student per course
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.student.user.username} → {self.course.title} ({self.rating}★)"


class Favourite(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="favourites")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "course")  # prevent duplicate favourites

    def __str__(self):
        return f"{self.student.user.username} ❤️ {self.course.title}"
    

class TrackEnrollment(models.Model):
    ENROLLMENT_TYPES = [
        ('free', 'Free'),
        ('paid', 'Paid'),
    ]

    student = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="enrollments")
    enrollment_type = models.CharField(max_length=10, choices=ENROLLMENT_TYPES, default='free')

    enrolled_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)  # for subscription/expiry

    class Meta:
        unique_together = ("student", "track")  # prevent duplicate enrollments

    def __str__(self):
        return f"{self.student.user.username} → {self.track.name} ({self.enrollment_type})"

    def can_access_chapter(self, course, chapter):
        """
        Business rule:
        - Paid students → full access
        - Free students → only chapters 1–3
        """
        if self.enrollment_type == "paid":
            return True

        # free access limit
        return chapter.order <= 3


class CourseProgress(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="progress_records")
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True, blank=True, related_name="progress_records")
    content = models.ForeignKey(Content, on_delete=models.SET_NULL, null=True, blank=True, related_name="progress_records")

    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "course", "content")

    def __str__(self):
        return f"{self.student.user.username} → {self.course.title} ({'Done' if self.completed else 'In Progress'})"


