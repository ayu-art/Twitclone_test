from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
  path('', views.TopView.as_view(), name='top'),
  path('data_input/', views.UserDataInput.as_view(), name='data_input'),
  path('data_confirm/', views.UserDataConfirm.as_view(), name='data_confirm'),
  path('data_save/', views.UserDataSave.as_view(), name='data_save'),
  path('profile/', views.ProfileView.as_view(), name='profile'),
  path('login/', views.LoginView.as_view(), name='login'),
]
