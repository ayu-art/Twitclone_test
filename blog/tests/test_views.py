from urllib.parse import urlencode
from django.conf import settings
from django.contrib.auth import login
from django.test import TestCase
from django.urls import reverse
from accounts.models import User

class NonLoginTweetTests(TestCase):
  def setUp(self):
    self.tweet_url = reverse('blog:tweet')
    self.login_url = reverse(settings.LOGIN_URL)
    self.login_redirect_url = f"{reverse(settings.LOGIN_URL)}?{urlencode({'next': self.tweet_url})}"

  # 未ログイン時にtweetviewにアクセスされるとログインページにリダイレクトされるか
  def test_non_login_tweet(self):
    self.response_get = self.client.get(self.tweet_url)
    self.assertRedirects(self.response_get, self.login_redirect_url, status_code=302, target_status_code=200)


class LoginTweetTests(TestCase):
  def setUp(self):
    self.top_url = reverse('blog:top')
    self.tweet_url = reverse('blog:tweet')
    self.login_url = reverse(settings.LOGIN_URL)
    User.objects.create_user('kinoko', 'kinoko123@gmail.com', 'kinopiko12')
    self.login_user = self.client.login(username='kinoko123@gmail.com', password='kinopiko12')
    self.user = User.objects.get(email='kinoko123@gmail.com')
    self.tweet_data = {
      'text': 'test1'
    }
    self.tweet_data2 = {
      'text': 'test2'
    }
    self.non_text_tweet_data = {
      'text': ''
    }
    self.long_tweet_data = {
      'text': 'あああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああ'
    }

  # ログイン後にツイート画面に遷移し、記事の投稿ができるか
  def test_successful_tweet(self):
    self.response_tweet = self.client.get(self.tweet_url)
    self.response_tweet_form = self.client.post(self.tweet_url, self.tweet_data)
    self.assertTrue(self.login_user)
    self.assertEquals(self.response_tweet.status_code, 200)
    self.assertTemplateUsed(self.response_tweet, 'blog/tweet.html')
    self.assertRedirects(self.response_tweet_form, self.top_url, status_code=302, target_status_code=200)

  # ツイートした時にテキストが空だと送信出来ず、エラーが発生するか
  def test_failure_form_empty(self):
    self.response_no_text_tweet = self.client.post(self.tweet_url, self.non_text_tweet_data)
    self.assertEquals(self.response_no_text_tweet.status_code, 200)
    form = self.response_no_text_tweet.context.get('form')
    self.assertTrue(form.errors)
    self.assertTemplateUsed(self.response_no_text_tweet, 'blog/tweet.html')
    self.assertFalse(self.user.post_set.exists())

  # ツイート後にcontextに名前・テキスト・時間が登録されているか。
  def test_successful_object_list(self):
    self.response_tweet_form = self.client.post(self.tweet_url, self.tweet_data)
    self.response_tweet_form2 = self.client.post(self.tweet_url, self.tweet_data2)
    self.assertQuerysetEqual(self.user.post_set.all(), ['<Post: test1>', '<Post: test2>'], ordered=False)
    self.assertTrue(self.user.post_set.filter(text='test1').exists())

  # 長いツイートを投稿してもデータベースに登録されない確認
  def test_failure_long_tweet(self):
    self.response_tweet_form = self.client.post(self.tweet_url, self.long_tweet_data)
    self.assertFalse(self.user.post_set.exists())


class TweetDeleteTests(TestCase):
  def setUp(self):
    self.top_url = reverse('blog:top')
    self.tweet_url = reverse('blog:tweet')
    self.login_url = reverse('accounts:login')
    User.objects.create_user('kinoko', 'kinoko123@gmail.com', 'kinopiko12')
    User.objects.create_user('kinopiko', 'kinopiko123@gmail.com', 'kinoko04')
    self.login_user = self.client.login(username='kinoko123@gmail.com', password='kinopiko12')
    self.user = User.objects.get(email='kinoko123@gmail.com')
    self.tweet_data = {
      'text': 'test1'
    }

  # deleteviewにpkを渡してきちんと削除できることの確認。また、削除した後それがhtml上から消えていることを確認。
  def test_successful_tweet_delete(self):
    self.response_tweet_form = self.client.post(self.tweet_url, self.tweet_data)
    self.response_top = self.client.get(self.top_url)
    self.pk = self.response_top.context['object_list'][0].pk
    self.delete_url = reverse('blog:tweet-delete', args=[self.pk])
    self.response_delete = self.client.post(self.delete_url)
    self.response_top = self.client.get(self.top_url)    
    self.assertRedirects(self.response_delete, self.top_url, status_code=302, target_status_code=200)
    self.assertFalse(self.user.post_set.exists())
    self.assertNotContains(self.response_top, 'test1')

  # 存在しないツイートを削除するとエラーがでるか
  def test_failure_not_exist_tweet(self):
    self.delete_url = reverse('blog:tweet-delete', args=[5])
    self.response_delete = self.client.post(self.delete_url)
    self.assertEqual(self.response_delete.status_code, 404)

  # 別のユーザーのツイートを削除するとエラーが出て削除されないことの確認
  def test_failure_different_user(self):
    self.response_tweet_form = self.client.post(self.tweet_url, self.tweet_data)
    self.client.logout()
    self.login_user2 = self.client.login(username='kinopiko123@gmail.com', password='kinoko04')
    self.response_top = self.client.get(self.top_url)
    self.pk = self.response_top.context['object_list'][0].pk
    self.delete_url = reverse('blog:tweet-delete', args=[self.pk])
    self.response_delete = self.client.post(self.delete_url)
    self.response_top = self.client.get(self.top_url)
    self.assertEqual(self.response_delete.status_code, 403)
    self.assertQuerysetEqual(self.user.post_set.all(), ['<Post: test1>'])
    self.assertContains(self.response_top, 'test1')  
