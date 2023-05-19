from rest_framework import serializers
from .models import Movie, Genre, Comment


class GenreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Genre
        fields = ('name',)

class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source = 'user.username', read_only = True)

    class Meta:
        model = Comment
        fields = ('content', 'created_at', 'updated_at', 'user_name', 'id')
        read_only_fields = ('movie',)

class MovieSerailizer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    comment_set = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'