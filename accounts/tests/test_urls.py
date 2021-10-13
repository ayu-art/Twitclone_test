from django.test import TestCase
from django.urls import reverse, resolve
from ..views import TopView, SignUpView, ProfileView


class UrlTests(TestCase):
  # top画面へのurlでアクセスする時のテスト
  def test_top_url(self):
    view = resolve('/accounts/')
    self.assertEqual(view.func.view_class, TopView)

  # signupへのurlでアクセスする時のテスト
  def test_signup_url(self):
    view = resolve('/accounts/signup/')
    self.assertEqual(view.func.view_class, SignUpView)

  # プロフィールへのurlでアクセスする時のテスト
  def test_profile_url(self):
    view = resolve('/accounts/profile/')
    self.assertEqual(view.func.view_class, ProfileView)
