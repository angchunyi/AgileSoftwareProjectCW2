from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)       # title (character field)
    file = models.FileField(upload_to="files")     # upload images
    content = models.TextField()                   # content
    date_posted = models.DateTimeField(default=timezone.now)     # date
    author = models.ForeignKey(User, on_delete=models.CASCADE)   # user
    # like post, include the User model
    likes = models.ManyToManyField(User, blank = True, related_name='likes')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})

# create a comment model to store all the comment
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

# create a contact model to store all the contact inputs by the user
class Contact(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField()
    message=models.TextField()
    def __str__(self):
        return self.name