from rest_framework.generics import ListCreateAPIView
from .models import FAQItem
from .serializers import FAQSerializer
from .permissions import OnlyAdminCreate

class FAQAPIView(ListCreateAPIView):
    queryset = FAQItem.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [OnlyAdminCreate]
