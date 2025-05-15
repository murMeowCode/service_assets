from rest_framework.routers import DefaultRouter
from notify.views import NotificationListBrowse

router = DefaultRouter()
router.register(r'notifications',NotificationListBrowse,basename='notifications')

urlpatterns=router.urls