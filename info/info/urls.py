"""
URL configuration for info project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from faq.views import FAQAPIView
from news.views import NewsItemListCreateView, CommentListCreateView
from achivments.views import AchivmentsListView, UserAchivmentsListView


urlpatterns = [
    path('achivments/', AchivmentsListView.as_view(), name='achivments-list'),
    path('faq/',FAQAPIView.as_view(),name='faq-list-create'),
    path('news/', NewsItemListCreateView.as_view(), name='news-list-create'),
    path('user-achivments/', UserAchivmentsListView.as_view(), name='user-achivments-list'),
    path('news/<int:news_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('',include('references.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
