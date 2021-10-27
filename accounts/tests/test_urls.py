from django.test import TestCase
from django.urls import reverse, resolve
from ..views import TopView, ProfileView, UserDataConfirm, UserDataInput, UserDataSave

class UrlTests(TestCase):
  # top画面へのurlでアクセスする時のテスト
  def test_top_url(self):
    view = resolve('/accounts/')
    self.assertEqual(view.func.view_class, TopView)

  # ユーザー登録フォームへアクセスするテスト
  def test_data_input_url(self):
    view = resolve('/accounts/data_input/')
    self.assertEqual(view.func.view_class, UserDataInput)

  # ユーザ確認にアクセスするテスト
  def test_data_confirm_url(self):
    view = resolve('/accounts/data_confirm/')
    self.assertEqual(view.func.view_class, UserDataConfirm)

  # ユーザ保存
  def test_data_save_url(self):
    view = resolve('/accounts/data_save/')
    self.assertEqual(view.func.view_class, UserDataSave)

  # プロフィールへのurlでアクセスする時のテスト
  def test_profile_url(self):
    view = resolve('/accounts/profile/')
    self.assertEqual(view.func.view_class, ProfileView)
