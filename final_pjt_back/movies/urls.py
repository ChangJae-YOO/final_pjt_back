from django.urls import path
from . import views

urlpatterns = [
     path('detail/<int:movie_pk>/', views.movie_detail),
     path('detail/<int:movie_pk>/comment_create/', views.comment_create),
     path('search/<str:search_str>/', views.search_movie),
     path('comments/<int:comment_pk>/', views.comment_detail),
     path('make_movies/', views.make_movies),
     path('make_genres/', views.make_genres),
]
