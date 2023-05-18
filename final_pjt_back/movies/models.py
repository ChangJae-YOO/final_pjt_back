from django.db import models

# Create your models here.
class Genre(models.Model):
    name = models.TextField()


class Movie(models.Model):
    title = models.CharField(max_length=100)
    adult = models.BooleanField()
    genres = models.ManyToManyField(Genre, related_name='movies')
    original_language = models.CharField(max_length=20)
    original_title = models.CharField(max_length=100)
    overview = models.TextField()
    popularity = models.FloatField()
    poster_path = models.TextField(null=True)
    release_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    runtime = models.FloatField()
    vote_average = models.FloatField()
    



    
