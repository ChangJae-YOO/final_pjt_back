from django.db import models
from django.conf import settings


class Theme(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    theme_likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_themes')
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(null=True)


class Question(models.Model):
    question = models.TextField()
    image = models.ImageField(null=True)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    

class AnswerQuery(models.Model):  # https://developer.themoviedb.org/reference/discover-movie 참고
    description = models.TextField()  # query 설명
    image = models.ImageField(null=True)

    include_adult = models.TextField(null=True)
    
    with_genres = models.TextField(null=True)
    without_genres = models.TextField(null=True)

    language = models.TextField(null=True)
    
    with_keywords = models.TextField(null=True)
    without_keywords = models.TextField(null=True)
    
    vote_average_gte = models.TextField(null=True)
    vote_average_lte = models.TextField(null=True)
    
    release_year = models.TextField(null=True)
    release_date_gte = models.TextField(null=True)
    release_date_lte = models.TextField(null=True)
    
    with_runtime_gte = models.TextField(null=True)
    with_runtime_lte = models.TextField(null=True)

    question = models.ForeignKey(Question, on_delete=models.CASCADE)