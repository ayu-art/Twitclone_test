from django.views.generic.edit import CreateView
from accounts.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.views.generic import TemplateView, FormView, CreateView
from .forms import LoginForm, SignUpForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

class TopView(TemplateView):
  template_name = 'accounts/top.html'


# ユーザ情報入力view
class UserDataInput(FormView):
  form_class = SignUpForm
  template_name = 'accounts/data_input.html'

  # confirm_htmlで戻るボタンを押されたときのみここに移る
  def form_valid(self, form):
    return render(self.request, 'accounts/data_input.html', {'form': form})


# ユーザ情報の確認。値が有効か否かでformを渡すhtmlを分ける
class UserDataConfirm(FormView):
  form_class = SignUpForm

  def form_valid(self, form):
    return render(self.request, 'accounts/data_confirm.html', {'form': form})

  def form_invalid(self, form):
    return render(self.request, 'accounts/data_input.html', {'form': form})


# 登録ボタンが押されたときにユーザデータ保存。
class UserDataSave(FormView):
  form_class = SignUpForm
  success_url = reverse_lazy('accounts:top')

  def form_valid(self, form):
    form.save()
    user = authenticate(
      email=form.cleaned_data['email'],
      password=form.cleaned_data['password1'],
      )
    login(self.request, user)
    return super().form_valid(form)

  # UserDataConfirmで値を判定しているので、普通はこない
  def form_invalid(self, form):
    return render(self.request, 'accounts/data_input.html', {'form': form})
    

class ProfileView(LoginRequiredMixin, TemplateView):
  template_name = 'accounts/profile.html'


class LoginView(LoginView):
  form_class = LoginForm
  template_name = 'accounts/login.html'
