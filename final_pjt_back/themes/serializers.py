from rest_framework import serializers
from .models import AnswerQuery, Theme, Question
from django.contrib.auth import get_user_model


class QuerySerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerQuery
        fields = '__all__'
        read_only_fields = ('question',)


class QuestionSerializer(serializers.ModelSerializer):
    answerquery_set = QuerySerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ('theme',)


class ThemeSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source = 'user.username', read_only = True)
    question_set = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Theme
        fields = '__all__'
        read_only_fields = ('user', 'theme_likes')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['like_user'] = []
        User = get_user_model()
        for user_id in rep['theme_likes']:
            rep['like_user'].append(User.objects.get(pk=user_id).username)
        return rep