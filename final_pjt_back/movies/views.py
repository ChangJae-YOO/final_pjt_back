from .models import Genre, Movie
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import GenreSerializer, MovieSerailizer
from rest_framework import status
import requests

# Create your views here.
@api_view(['GET'])
def movie_detail(request, movie_pk):

    movie = Movie.objects.get(pk = movie_pk)
    serializer = MovieSerailizer(movie)
    return Response(serializer.data)

@api_view(['GET'])
def make_movies(request):

    for id in range(100, 1000):
        response = requests.get(f"https://api.themoviedb.org/3/movie/{id}?language=ko-KR&api_key=f71b3408ea6ab0e8ac8a36b985605a43")
        json_movie = response.json()

        if 'success' in json_movie:
            continue

        movie = Movie.objects.create(
            id = json_movie['id'],
            title = json_movie['title'],
            adult = json_movie['adult'],
            original_language = json_movie['original_language'], 
            original_title = json_movie['original_title'],
            overview = json_movie['overview'],
            popularity = json_movie['popularity'],
            poster_path = json_movie['poster_path'],
            release_date = json_movie['release_date'],
            runtime = json_movie['runtime'],
            vote_average = json_movie['vote_average'],
        )

        for genre_info in json_movie['genres']:
            genre = Genre.objects.get(id = genre_info['id'])
            movie.genres.add(genre)

    return Response("hi")

@api_view(['GET'])
def make_genres(request):

    response = requests.get('https://api.themoviedb.org/3/genre/movie/list?language=ko-KR&api_key=f71b3408ea6ab0e8ac8a36b985605a43')
    genres = response.json()
    for genre_info in genres['genres']:
        Genre.objects.create(
            id = genre_info['id'],
            name = genre_info['name']
        )

    return Response("good")
