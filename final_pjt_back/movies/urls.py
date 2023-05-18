from django.urls import path
from . import views

urlpatterns = [
     path('detail/<int:movie_pk>/', views.movie_detail),
     path('make_movies/', views.make_movies),
     path('make_genres/', views.make_genres),
]
