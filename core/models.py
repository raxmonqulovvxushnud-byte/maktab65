
from django.db import models
from django.conf import settings


class SchoolInfo(models.Model):
    title = models.CharField(max_length=200, default="65-Maktab")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="school/", blank=True, null=True)

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="news/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"

    def __str__(self):
        return self.title


class Gallery(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="gallery/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Galereya rasmi"
        verbose_name_plural = "Fotogalereya"

    def __str__(self):
        return self.title


class UserProfile(models.Model):

    class Role(models.TextChoices):
        STUDENT = "student", "O'quvchi"
        TEACHER = "teacher", "O'qituvchi"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    role = models.CharField(
        max_length=10,
        choices=Role.choices
    )

    grade = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="Sinf"
    )

    subject = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Fan"
    )

    is_approved = models.BooleanField(
        default=False,
        verbose_name="Tasdiqlangan"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Foydalanuvchi profili"
        verbose_name_plural = "Foydalanuvchilar"

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
