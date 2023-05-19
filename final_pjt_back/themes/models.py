from django.db import models
from django.conf import settings


class Theme(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    theme_likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_themes')
    title = models.CharField(max_length=100)
    description = models.TextField()


class Query(models.Model):  # https://developer.themoviedb.org/reference/discover-movie 참고
    description = models.TextField()  # query 설명

    include_adult = models.BooleanField()
    
    with_genres = models.TextField()
    without_genres = models.TextField()

    language = models.CharField(max_length=20)
    
    with_keywords = models.TextField()
    without_keywords = models.TextField()
    
    vote_average_gte = models.FloatField()
    vote_average_lte = models.FloatField()
    
    release_year = models.IntegerField()
    release_date_gte = models.DateTimeField()
    release_date_lte = models.DateTimeField()
    
    with_runtime_gte = models.IntegerField()
    with_runtime_lte = models.IntegerField()
    
    sort_by = models.CharField(max_length=50)

    with_crew = models.TextField()

    themes = models.ForeignKey(Theme, on_delete=models.CASCADE)