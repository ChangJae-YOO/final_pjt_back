from rest_framework import serializers
from .models import Query, Theme

class ThemeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Theme
        fields = ('title', 'description', 'user')
        read_only_fields = ('user',)

class QuerySerializer(serializers.ModelSerializer):

    class Meta:
        model = Query
        fields = '__all__'
        read_only_fields = ('user', 'theme')