from django.urls import path
from . import views

urlpatterns = [
     path('detail/<int:movie_pk>/', views.movie_detail),  # 영화 상세정보

     path('detail/<int:movie_pk>/comment_create/', views.comment_create),  # 영화에 댓글 달기
     path('comments/<int:comment_pk>/', views.comment_detail),  # 영화의 달린 댓글의 수정, 삭제, 보기
     path('comments/<int:comment_pk>/like_comment/', views.like_comment),  # 영화의 달린 댓글의 수정, 삭제, 보기
     
     path('detail/<int:movie_pk>/like_movie/', views.like_movie),  # 영화 좋아요
     path('detail/<int:movie_pk>/hate_movie/', views.hate_movie),  # 영화 싫어요
     path('detail/<int:movie_pk>/viewed_movie/', views.viewed_movie),  # 영화 봤어요
     
     path('search/<str:search_str>/', views.search_movie),  # 영화 검색
     path('get_movies/', views.get_movies),

     path('make_movies/', views.make_movies),  # db에 영화 정보를 채워넣기 위한 url, 배포시엔 주석화 해야됨
     path('make_genres/', views.make_genres),  # db에 장르 정보를 채워넣기 위한 url, 배포시엔 주석화 해야됨
]
