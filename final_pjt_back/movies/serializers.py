from rest_framework import serializers
from .models import Movie, Genre, Comment
from django.contrib.auth import get_user_model



class GenreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Genre
        fields = ('name',)


class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source = 'user.username', read_only = True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('movie', 'comment_likes', 'user')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['comment_user'] = []
        User = get_user_model()
        for user_id in rep['comment_likes']:
            rep['comment_user'].append(User.objects.get(pk=user_id).username)
        return rep

class MovieSerailizer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    comment_set = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'