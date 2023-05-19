from rest_framework import serializers
from .models import Query, Theme

class ThemeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Theme
        fields = ('title', 'description', 'user')
        read_only_fields = ('user',)
