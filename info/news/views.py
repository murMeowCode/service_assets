from rest_framework import generics, permissions
from .models import NewsItem, Comment
from .serializers import NewsItemSerializer, CommentSerializer
from faq.permissions import OnlyAdminCreate  # Импортируем ваше кастомное разрешение

class NewsItemListCreateView(generics.ListCreateAPIView):
    queryset = NewsItem.objects.all()
    serializer_class = NewsItemSerializer
    permission_classes = [OnlyAdminCreate]


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        news_id = self.kwargs['news_id']
        return Comment.objects.filter(pk=news_id)

    def perform_create(self, serializer):
        news_id = self.kwargs['news_id']
        serializer.save(
            news_item=news_id,
            author=self.request.user.username  # Или user=self.request.user если связь с User
        )