# View 객체 생성
from .models import Theme, AnswerQuery, Question
from .serializers import ThemeSerializer, QuerySerializer, QuestionSerializer

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


# 테마 리스트를 가져오거나 테마를 생성한다.
@api_view(['GET', 'POST'])
def theme(request):
    
    if request.method == 'GET':
        themes = Theme.objects.all()
        serializer = ThemeSerializer(themes, many=True)
        return Response(serializer.data)

    if request.method == 'POST' and request.user.is_authenticated:
        serializer = ThemeSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_400_BAD_REQUEST)


# 테마 디테일, 수정, 삭제
@api_view(['GET', 'DELETE', 'PUT'])
def theme_detail(request, theme_pk):
    theme = get_object_or_404(Theme, pk=theme_pk)
    user = request.user

    if request.method == 'GET':
        serializer = ThemeSerializer(theme)
        return Response(serializer.data)

    elif request.method == 'DELETE' and theme.user == user:
        theme.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT' and theme.user == user:
        serializer = ThemeSerializer(theme, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


# 테마 좋아요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_theme(request, theme_pk):
    theme = get_object_or_404(Theme, pk=theme_pk)
    user = request.user

    if theme.theme_likes.filter(pk=user.pk).exists():
        theme.theme_likes.remove(user)
        is_liked = False
    else:
        theme.theme_likes.add(user)
        is_liked = True
    
    context = {
        'is_liked':is_liked,
        'like_count': theme.theme_likes.count(),
    }

    return JsonResponse(context)


# 테마에 질문를 생성한다.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_question(request, theme_pk):
    theme = get_object_or_404(Theme, pk = theme_pk)
    serializer = QuestionSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save(theme = theme)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 테마에 달린 질문을 삭제, 수정, 보는 부분
@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def question_detail(request, question_pk):
    query = get_object_or_404(Question, pk=question_pk)

    if request.method == 'GET':
        serializer = QuestionSerializer(query)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = QuestionSerializer(query, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


# 질문에 쿼리를 생성한다.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_query(request, question_pk):
    question = get_object_or_404(Question, pk = question_pk)
    serializer = QuerySerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save(question = question)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 질문에 달린 쿼리를 삭제, 수정, 보는 부분
@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def query_detail(request, query_pk):
    query = get_object_or_404(AnswerQuery, pk=query_pk)

    if request.method == 'GET':
        serializer = QuerySerializer(query)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = QuerySerializer(query, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST'])
def get_movies(request):
    
    features = request.POST
    print(features)

    key_match = {
        'with_genres': 'with_genres',
        'without_genres': 'without_genres',

        'language': 'language',

        'with_keywords': 'with_keywords',
        'without_keywords': 'without_keywords',
        
        'vote_average_gte': 'vote_average.gte',
        'vote_average_lte': 'vote_average.lte',
        
        'release_year': 'release_year',
        'release_date_gte': 'release_date.gte',
        'release_date_lte': 'release_date.lte',
        
        'with_runtime_gte': 'with_runtime.gte',
        'with_runtime_lte': 'with_runtime.lte',
        
        'sort_by': 'sort_by',

        'with_crew': 'with_crew',
    }

    url = 'https://api.themoviedb.org/3/discover/movie?page=1'
    Authorization = 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmNzFiMzQwOGVhNmFiMGU4YWM4YTM2Yjk4NTYwNWE0MyIsInN1YiI6IjYzZDIwM2M4YTQxMGM4MTFmOWUwMWM5ZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Io1ZK_1UZP3n6DOzMzbn-OqstYSopJ2V4g6Jp6_D5e0'
    accept = 'application/json'

    print(features)

    for key in features:

        if key not in key_match:
            continue

        temp_query = '&' + str(key_match[key]) + '='

        for params in features[key]:
            temp_query += str(params)

        url += temp_query

    headers = {
        'Authorization': Authorization,
        'accept': accept,
    }

    response = requests.get(url, headers=headers)
    return JsonResponse(response.json())



