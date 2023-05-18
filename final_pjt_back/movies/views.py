from .models import Genre, Movie, Comment
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import GenreSerializer, MovieSerailizer, CommentSerializer
from rest_framework import status
import requests
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404

# id = movie_pk 에 해당하는 영화의 세부사항을 반환한다.
@api_view(['GET'])
def movie_detail(request, movie_pk):

    movie = Movie.objects.get(pk = movie_pk)
    serializer = MovieSerailizer(movie)
    return Response(serializer.data)

# search_str 을 포함하는 제목을 가진 영화들을 반환한다.
@api_view(['GET'])
def search_movie(request, search_str):
    movies_title = Movie.objects.filter(title__contains = search_str)
    movies_original_title = Movie.objects.filter(original_title__contains = search_str)
    movies = movies_title.union(movies_original_title)
    movie_lst = []

    for movie in movies:
        movie_lst.append(MovieSerailizer(movie).data)

    return JsonResponse(movie_lst, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, movie_pk):
    movie = Movie.objects.get(pk = movie_pk)
    serializer = CommentSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save(movie = movie, user = request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'DELETE', 'PUT'])
def comment_detail(request, comment_pk):
    # comment = Comment.objects.get(pk=comment_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)



# db에 영화 정보를 채운다.
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

    return Response("good")

# db에 장르 정보를 채운다.
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
