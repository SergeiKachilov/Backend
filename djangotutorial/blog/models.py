from django.db import models

# Create your models here.

class Blog(models.Model):
    blog_name = models.CharField(max_length=100)
    blog_text = models.TextField(max_length=1000)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.blog_text

class User(models.Model):
    login = models.CharField(max_length=20)
    password = models.CharField()

    def __str__(self):
        return self.login

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=500)

    def __str__(self):
        return self.comment_text