from django.db import models
from django.utils import timezone


class LeafImage(models.Model):
    image = models.ImageField(upload_to='leaf_images/')
    predicted_disease = models.CharField(max_length=100, blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.predicted_disease or 'Not Predicted'} - {self.image.name}"



from ckeditor.fields import RichTextField

class Blog(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    content = RichTextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Reaction(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=20)  # like, love, angry, etc.

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"