from django.urls import path
from references.views import RoleListAPIView, VipAPIView

urlpatterns = [
    path('roles/',RoleListAPIView.as_view(),name='role-list'),
    path('vip/<int:id>/',VipAPIView.as_view(),name='vip_statuses')
]
