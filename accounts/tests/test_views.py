from django.test import TestCase
from django.urls import reverse

class TopTests(TestCase):
  def setUp(self):
    url = reverse('accounts:top')
    self.response = self.client.get(url)

  def test_top_status_code(self):
    self.assertEqual(self.response.status_code, 200)

  
class SuccessSignUpTests(TestCase):
  def setUp(self):
    url = reverse('accounts:signup')
    data= {
      'username': 'kinoko',
      'email': 'testemail49@gmail.com',
      'password1': 'kokoatest1',
      'password2': 'kokoatest1'
    }
    # data1はフォームで確認ボタンを押したとき、data2は登録確認画面で登録ボタンを押したとき、data3は登録確認画面で戻るボタンを押したときのもの。
    data1 = {'next': 'confirm'}
    data1.update(data)
    data2 = {'next': 'regist'}
    data2.update(data)
    data3 = {'next': 'back'}
    data3.update(data)
    self.response1 = self.client.post(url, data1)
    self.response2 = self.client.post(url, data2)
    self.response3 = self.client.post(url, data3)
    self.homeurl = reverse('accounts:top')

  def test_post_confirm_status_code(self):
    self.assertEqual(self.response1.status_code, 200)

  # 登録ボタンを押したときにリダイレクトして最初のページに戻るかの確認。
  def test_post_regist_redirect(self):
    self.assertRedirects(self.response2, self.homeurl ,status_code=302, target_status_code=200)

  def test_post_back_status_code(self):
    self.assertEqual(self.response3.status_code, 200)
  
  # エラーメッセージが発生しないことを確認
  def test_form_noerrors(self):
    form = self.response1.context.get('form')
    self.assertFalse(form.errors)

  # 新規登録してユーザーが認証済みになったかの確認
  def test_user_authenticated(self):
    response = self.client.get(self.homeurl)
    user = response.context.get('user')
    self.assertTrue(user.is_authenticated)


class FailSignUpTests(TestCase):
  def setUp(self):
    url = reverse('accounts:signup')
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
    data_confirm = {'next': 'confirm'}
    data1.update(data_confirm)
    data2.update(data_confirm)
    data3.update(data_confirm)
    self.response1 = self.client.post(url, data1)
    self.response2 = self.client.post(url, data2)
    self.response3 = self.client.post(url, data3)

  def test_signup_status_code(self):
    self.assertEquals(self.response1.status_code, 200)
    self.assertEquals(self.response2.status_code, 200)
    self.assertEquals(self.response3.status_code, 200)

  # エラーが発生することを確認
  def test_form_errors(self):
    form1 = self.response1.context.get('form')
    self.assertTrue(form1.errors)
    form2 = self.response2.context.get('form')
    self.assertTrue(form2.errors)
    form3 = self.response3.context.get('form')
    self.assertTrue(form3.errors)
