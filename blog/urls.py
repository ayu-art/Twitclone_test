from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
  path('', views.TopView.as_view(), name='top'),
  path('tweet/', views.TweetView.as_view(), name='tweet'),
]
