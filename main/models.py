from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=200)
    github_url = models.URLField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="projects/", blank=True, null=True)

    def __str__(self):
        return self.title


class Certificate(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="certificates/")
    is_archived = models.BooleanField(default=False, verbose_name='В архиве')

    def __str__(self):
        return self.title


class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.email}"


class Award(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="awards/")

    def __str__(self):
        return self.title