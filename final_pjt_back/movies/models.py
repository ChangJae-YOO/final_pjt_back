from django.db import models
from django.conf import settings

# 장르 모델 (ERD 참고)
class Genre(models.Model):
    name = models.TextField()  # 장르 이름


# 영화 모델 (ERD 참고)
class Movie(models.Model):
    title = models.CharField(max_length=100)
    adult = models.BooleanField()
    genres = models.ManyToManyField(Genre, related_name='movies')
    original_language = models.CharField(max_length=20)
    original_title = models.CharField(max_length=100)
    overview = models.TextField(null=True)
    popularity = models.FloatField(null=True)
    poster_path = models.TextField(null=True)
    backdrop_path = models.TextField(null=True)
    tagline = models.TextField(null=True)
    release_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    runtime = models.FloatField(null=True)
    vote_average = models.FloatField(null=True)
    movie_likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
    movie_hates = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='hate_movies')
    movie_viewd = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='viewed_movies')

# 댓글 모델 (ERD 참고)
class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment_likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    



    
