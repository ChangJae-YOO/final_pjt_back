from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.theme),
    path('detail/<int:theme_pk>/', views.theme_detail),
    path('detail/<int:theme_pk>/like_theme/', views.like_theme),

    path('detail/<int:theme_pk>/create_question/', views.create_question),
    path('detail/<int:question_pk>/create_query/', views.create_query),
    path('detail/<int:theme_pk>/get_movies/', views.get_movies),
    path('question/<int:question_pk>/', views.question_detail),
    path('query/<int:query_pk>/', views.query_detail),
]
