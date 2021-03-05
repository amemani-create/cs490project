from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = RichTextField(blank=True, null=True)
    #content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    #snippet = models.CharField(max_length=200, default=content)
    tags = TaggableManager()
    likes = models.ManyToManyField(User, related_name='blogpost_like')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title + '|' + str(self.author_id)

    def get_absolute_url(self):
        return reverse('post_detail', args=(str(self.id)))

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return 'Comment {} by {}'.format(self.comment, self.author)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    bio = models.TextField()
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    linkedin_url = models.CharField(max_length=200, null=True, blank=True)
    fb_url = models.CharField(max_length=200, null=True, blank=True)
    instagram_url = models.CharField(max_length=200, null=True, blank=True)
    personal_url = models.CharField(max_length=200, null=True, blank=True)

    #user_type = models.CharField(max_length=255, default='Parent')
    #school_level_pref = models.ManyToManyField()

    def __str__(self):
        return str(self.user)