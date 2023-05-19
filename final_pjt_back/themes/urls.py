from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.theme),
    path('detail/<int:theme_pk>/', views.theme_detail),
    path('detail/<int:theme_pk>/like_theme/', views.like_theme),
]
