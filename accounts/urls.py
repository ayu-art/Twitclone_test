from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
  path('data-input/', views.UserDataInput.as_view(), name='data-input'),
  path('data-confirm/', views.UserDataConfirm.as_view(), name='data-confirm'),
  path('data-save/', views.UserDataSave.as_view(), name='data-save'),
  path('profile/', views.ProfileView.as_view(), name='profile'),
  path('login/', views.LoginView.as_view(), name='login'),
  path('logout-confirm/', views.LogoutConfirmView.as_view(), name='logout-confirm'),
  path('logout/', views.LogoutView.as_view(), name='logout'),
]
