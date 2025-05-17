from django.urls import path
from references.views import RoleListAPIView

urlpatterns = [
    path('roles/',RoleListAPIView.as_view(),name='role-list'),
]
