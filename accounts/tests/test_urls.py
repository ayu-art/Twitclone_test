from django.test import TestCase
from django.urls import reverse, resolve
from ..views import TopView, ProfileView, UserDataConfirm, UserDataInput, UserDataSave, LoginView, LogoutConfirmView, LogoutView

class UrlTests(TestCase):
  # top画面へのurlでアクセスする時のテスト
  def test_top_url(self):
    view = resolve('/accounts/')
    self.assertEqual(view.func.view_class, TopView)

  # ユーザー登録フォームへアクセスするテスト
  def test_data_input_url(self):
    view = resolve('/accounts/data-input/')
    self.assertEqual(view.func.view_class, UserDataInput)

  # ユーザ確認にアクセスするテスト
  def test_data_confirm_url(self):
    view = resolve('/accounts/data-confirm/')
    self.assertEqual(view.func.view_class, UserDataConfirm)

  # ユーザ保存
  def test_data_save_url(self):
    view = resolve('/accounts/data-save/')
    self.assertEqual(view.func.view_class, UserDataSave)

  # プロフィールへのurlでアクセスする時のテスト
  def test_profile_url(self):
    view = resolve('/accounts/profile/')
    self.assertEqual(view.func.view_class, ProfileView)

  def test_login_url(self):
    view = resolve('/accounts/login/')
    self.assertEqual(view.func.view_class, LoginView)

  def test_logout_confirm_url(self):
    view = resolve('/accounts/logout-confirm/')
    self.assertEqual(view.func.view_class, LogoutConfirmView)

  def test_logout_url(self):
    view = resolve('/accounts/logout/')
    self.assertEqual(view.func.view_class, LogoutView)
