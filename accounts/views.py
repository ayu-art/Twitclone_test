from accounts.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

class TopView(TemplateView):
  template_name = 'accounts/top.html'


class SignUpView(FormView):
  form_class = SignUpForm
  template_name = 'accounts/signup.html'
  success_url = reverse_lazy('accounts:top')

  def form_valid(self, form):
    if self.request.POST['next'] == 'back':
      return render(self.request, 'accounts/signup.html', {'form': form})
    elif self.request.POST['next'] == 'confirm':
      return render(self.request, 'accounts/confirm.html', {'form': form})
    elif self.request.POST['next'] == 'regist':
      form.save()
      user = authenticate(
        email=form.cleaned_data['email'],
        password=form.cleaned_data['password1'],
        )
      login(self.request, user)
      return super().form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
  template_name = 'accounts/profile.html'

  def get_queryset(self):
    return User.objects.get(id=self.request.user.id)
