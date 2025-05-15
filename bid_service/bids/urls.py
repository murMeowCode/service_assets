from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BidViewSet

router = DefaultRouter()
router.register(r'bids', BidViewSet,basename='bids')
urlpatterns = router.urls