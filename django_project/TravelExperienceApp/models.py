from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    # title (character field)
    title = models.CharField(max_length=100)
    # upload images
    image = models.ImageField(upload_to="images")
    # content
    content = models.TextField()
    # date
    date_posted = models.DateTimeField(default=timezone.now)
    # user
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # like post
    likes = models.ManyToManyField(User, blank = True, related_name='likes')
    # dislike post
    dislikes = models.ManyToManyField(User, blank = True, related_name='dislikes')


    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

class Contact(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField()
    message=models.TextField()

    def __str__(self):
        return self.name