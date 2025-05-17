from rest_framework import serializers
from .models import NewsItem, Comment

class NewsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsItem
        fields = '__all__'
        read_only_fields = ('created_at',)

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)  # Чтобы нельзя было подменить автора
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('created_at', 'news_item', 'author')