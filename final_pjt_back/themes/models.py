from django.db import models
from django.conf import settings


class Theme(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    theme_likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_themes')
    title = models.CharField(max_length=100)
    description = models.TextField()


class Query(models.Model):  # https://developer.themoviedb.org/reference/discover-movie 참고
    description = models.TextField()  # query 설명

    include_adult = models.CharField(max_length=10, null=True)
    
    with_genres = models.TextField(null=True)
    without_genres = models.TextField(null=True)

    language = models.CharField(max_length=20, null=True)
    
    with_keywords = models.TextField(null=True)
    without_keywords = models.TextField(null=True)
    
    vote_average_gte = models.FloatField(null=True)
    vote_average_lte = models.FloatField(null=True)
    
    release_year = models.IntegerField(null=True)
    release_date_gte = models.DateTimeField(null=True)
    release_date_lte = models.DateTimeField(null=True)
    
    with_runtime_gte = models.IntegerField(null=True)
    with_runtime_lte = models.IntegerField(null=True)
    
    sort_by = models.CharField(max_length=50, null=True)

    with_crew = models.TextField(null=True)

    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)