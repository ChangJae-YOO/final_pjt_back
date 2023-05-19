# View 객체 생성
from .models import Genre, Movie, Comment
from .serializers import GenreSerializer, MovieSerailizer, CommentSerializer

# View 요청 응답
import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.http import JsonResponse
from rest_framework.response import Response

# django 사용자 인증
from rest_framework.decorators import permission_classes


# id = movie_pk 에 해당하는 영화의 세부사항을 반환한다.
@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk = movie_pk)
    serializer = MovieSerailizer(movie)
    return Response(serializer.data)


# 영화에 댓글을 생성한다.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk = movie_pk)
    serializer = CommentSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save(movie = movie, user = request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 영화에 달린 댓글을 삭제, 수정, 보는 부분
@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    user = request.user

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'DELETE' and comment.user == user:
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT' and comment.user == user:
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


# 댓글 좋아요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_comment(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    user = request.user

    if comment.comment_likes.filter(pk=user.pk).exists():
        comment.comment_likes.remove(user)
        is_liked = False
    else:
        comment.comment_likes.add(user)
        is_liked = True
    
    context = {
        'is_liked':is_liked,
        'like_count': comment.comment_likes.count(),
    }

    return JsonResponse(context)



# 영화 좋아요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_movie(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user

    if movie.movie_likes.filter(pk=user.pk).exists():
        movie.movie_likes.remove(user)
        is_liked = False
    else:
        movie.movie_likes.add(user)
        is_liked = True
    
    context = {
        'is_liked':is_liked,
        'like_count': movie.movie_likes.count(),
    }

    return JsonResponse(context)


# 영화 싫어요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def hate_movie(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user

    if movie.movie_hates.filter(pk=user.pk).exists():
        movie.movie_hates.remove(user)
        is_hated = False
    else:
        movie.movie_hates.add(user)
        is_hated = True
    
    context = {
        'is_hated':is_hated,
        'hate_count': movie.movie_hates.count(),
    }

    return JsonResponse(context)


# 영화 봤어요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def viewed_movie(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user

    if movie.movie_viewd.filter(pk=user.pk).exists():
        movie.movie_viewd.remove(user)
        is_viewed = False
    else:
        movie.movie_viewd.add(user)
        is_viewed = True
    
    context = {
        'is_viewed':is_viewed,
        'viewed_count': movie.movie_viewd.count(),
    }

    return JsonResponse(context)



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
