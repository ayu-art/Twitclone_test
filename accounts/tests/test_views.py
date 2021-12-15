from django.contrib.auth import login
from django.test import TestCase
from django.urls import reverse
from accounts.models import User

class TopTests(TestCase):
  def setUp(self):
    url = reverse('accounts:top')
    self.response = self.client.get(url)

  def test_top_status_code(self):
    self.assertEqual(self.response.status_code, 200)

  
class SuccessSignUpTests(TestCase):
  def setUp(self):
    url1 = reverse('accounts:data-input')
    url2 = reverse('accounts:data-confirm')
    url3 = reverse('accounts:data-save')
    data= {
      'username': 'kinoko',
      'email': 'testemail49@gmail.com',
      'password1': 'kokoatest1',
      'password2': 'kokoatest1'
    }
    # response1は戻るボタンを押したとき、respons2は確認ボタンを押したとき、response3は登録ボタンを押したとき
    self.response1 = self.client.post(url1, data)
    self.response2 = self.client.post(url2, data)
    self.response3 = self.client.post(url3, data)
    self.top_url = reverse('accounts:top')

  # 確認画面にいけるかの確認
  def test_post_confirm_status_code(self):
    self.assertEqual(self.response1.status_code, 200)
    self.assertTemplateUsed(self.response2, 'accounts/data_confirm.html')

  # 登録ボタンを押したときにリダイレクトして最初のページに戻るかの確認。
  def test_post_regist_redirect(self):
    self.assertRedirects(self.response3, self.top_url ,status_code=302, target_status_code=200)

  def test_post_back_status_code(self):
    self.assertEqual(self.response1.status_code, 200)
  
  # エラーメッセージが発生しないことを確認
  def test_form_noerrors(self):
    form = self.response2.context.get('form')
    self.assertFalse(form.errors)

  # 新規登録してユーザーが認証済みになったかの確認
  def test_user_authenticated(self):
    response = self.client.get(self.top_url)
    user = response.context.get('user')
    self.assertTrue(user.is_authenticated)


class FailSignUpTests(TestCase):
  def setUp(self):
    url = reverse('accounts:data-confirm')
    # data1は無効なメールアドレス、data2は異なるパスワード、data3は記入漏れがある場合のデータ
    data1 = {
      'username': 'kinoko',
      'email': 'testemail@@@gmail.com',
      'password1': 'kinokotest1',
      'password2': 'kinokotest1'
    }
    data2 = {
      'username': 'kinoko',
      'email': 'testemail@gmail.com',
      'password1': 'kokoatest1',
      'password2': 'kokoatest2'
    }
    data3 = {
      'username': 'kinoko',
      'email': '',
      'password1': 'kokoatest1',
      'password2': 'kokoatest1'
    }
    self.response1 = self.client.post(url, data1)
    self.response2 = self.client.post(url, data2)
    self.response3 = self.client.post(url, data3)

  # 無効なメールアドレスの確認、data_input.htmlに行く確認
  def test_invalid_email(self):
    self.assertEquals(self.response1.status_code, 200)
    form1 = self.response1.context.get('form')
    self.assertTrue(form1.errors)
    self.assertTemplateUsed(self.response1, 'accounts/data_input.html')

  # 異なるパスワードを入れた時の確認
  def test_invalid_password(self):
    self.assertEquals(self.response2.status_code, 200)
    form2 = self.response2.context.get('form')
    self.assertTrue(form2.errors)
    self.assertTemplateUsed(self.response２, 'accounts/data_input.html')

  # 記入漏れがあるときの確認
  def test_empty_form(self):
    self.assertEquals(self.response3.status_code, 200)
    form3 = self.response3.context.get('form')
    self.assertTrue(form3.errors)
    self.assertTemplateUsed(self.response3, 'accounts/data_input.html')


class SuccessLoginTests(TestCase):
  def setUp(self):
    self.user = User.objects.create_user('kinoko', 'kinoko123@gmail.com', 'kinopiko12')
    login_url = reverse('accounts:login')
    data = {
      'username': 'kinoko123@gmail.com',
      'password': 'kinopiko12'
    }
    self.response_get = self.client.get(login_url)
    self.response_post = self.client.post(login_url, data)
    self.top_url = reverse('accounts:top')

  # データを渡さずloginviewにアクセスされたとき、login.htmlが表示されるか
  def test_login_status_code(self):
    self.assertEqual(self.response_get.status_code, 200)
    self.assertTemplateUsed(self.response_get, 'accounts/login.html')

  # ログインした後にtopページにリダイレクトされるか
  def test_login_redirect(self):
    self.assertRedirects(self.response_post, self.top_url ,status_code=302, target_status_code=200)


class FailLoginTests(TestCase):
  def setUp(self):
    self.user = User.objects.create_user('kinoko', 'kinoko123@gmail.com', 'kinopiko12')
    self.login_url = reverse('accounts:login')
    # data1は異なるメールアドレス、data2は記入漏れがある場合
    self.data1 = {
      'username': 'kinoko000@gmail.com',
      'password': 'kinopiko12'
    }
    self.data2 = {
      'username': 'kinoko123@gmail.com',
      'password': ''
    }

  # 認証されないとエラーが出て、top.htmlにリダイレクトされないことの確認
  def test_different_email(self):
    self.response_email = self.client.post(self.login_url, self.data1)
    self.assertEquals(self.response_email.status_code, 200)
    form1 = self.response_email.context.get('form')
    self.assertTrue(form1.errors)
    self.assertTemplateUsed(self.response_email, 'accounts/login.html')

  def test_password_empty(self):
    self.response_empty_form = self.client.post(self.login_url, self.data2)
    self.assertEquals(self.response_empty_form.status_code, 200)
    form1 = self.response_empty_form.context.get('form')
    self.assertTrue(form1.errors)
    self.assertTemplateUsed(self.response_empty_form, 'accounts/login.html')


class LogoutTests(TestCase):
  def setUp(self):
    self.user = User.objects.create_user('kinoko', 'kinoko123@gmail.com', 'kinopiko12')
    self.login_user = self.client.login(username='kinoko', password='kinopiko12')
    url1 = reverse('accounts:logout-confirm')
    url2 = reverse('accounts:logout')
    self.response_confirm = self.client.get(url1)
    self.response_logout = self.client.get(url2)

  # ログアウトの確認画面にいけるかの確認
  def test_logout_confirm(self):
    self.assertEqual(self.response_confirm.status_code, 200)
    self.assertTemplateUsed(self.response_confirm, 'accounts/logout_confirm.html')

  # ログアウトが出来たかの確認
  def test_logout(self):
    self.assertEqual(self.response_logout.status_code, 200)
    self.assertTemplateUsed(self.response_logout, 'accounts/logout.html')
    self.assertFalse('username' in self.response_logout)
