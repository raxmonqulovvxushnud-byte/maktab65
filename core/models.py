from django.db import models


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
