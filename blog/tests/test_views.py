from operator import index
from django.contrib.auth import login
from django.test import TestCase
from django.urls import reverse
from accounts.models import User

class NonLoginTweetTests(TestCase):
  def setUp(self):
    self.tweet_url = reverse('blog:tweet')
    self.login_url = reverse('accounts:login')
    self.login_redirect_url = '/accounts/login/?next=/blog/tweet/'

  # 未ログイン時にtweetviewにアクセスされるとログインページにリダイレクトされるか
  def test_non_login_tweet(self):
    self.response_get = self.client.get(self.tweet_url)
    self.assertRedirects(self.response_get, self.login_redirect_url, status_code=302, target_status_code=200)


class LoginTweetTests(TestCase):
  def setUp(self):
    self.top_url = reverse('blog:top')
    self.tweet_url = reverse('blog:tweet')
    self.login_url = reverse('accounts:login')
    self.user = User.objects.create_user('kinoko', 'kinoko123@gmail.com', 'kinopiko12')
    self.login_user = self.client.login(username='kinoko123@gmail.com', password='kinopiko12')
    self.tweet_data = {
      'text': 'test1'
    }
    self.tweet_data2 = {
      'text': 'test2'
    }
    self.non_text_tweet_data = {
      'text': ''
    }
    self.response_tweet = self.client.get(self.tweet_url)
    self.response_tweet_form = self.client.post(self.tweet_url, self.tweet_data)
    self.response_tweet_form2 = self.client.post(self.tweet_url, self.tweet_data2)
    self.response_no_text_tweet = self.client.post(self.tweet_url, self.non_text_tweet_data)
    self.response_top = self.client.get(self.top_url)

  # ログイン後にツイート画面に遷移し、記事の投稿ができるか
  def test_successful_tweet(self):
    self.assertTrue(self.login_user)
    self.assertEquals(self.response_tweet.status_code, 200)
    self.assertTemplateUsed(self.response_tweet, 'blog/tweet.html')
    self.assertRedirects(self.response_tweet_form, self.top_url, status_code=302, target_status_code=200)

  # ツイートした時にテキストが空だと送信出来ず、エラーが発生するか
  def test_form_empty(self):
    self.assertEquals(self.response_no_text_tweet.status_code, 200)
    form = self.response_no_text_tweet.context.get('form')
    self.assertTrue(form.errors)
    self.assertTemplateUsed(self.response_no_text_tweet, 'blog/tweet.html')

  # ツイート後にcontextに名前・テキスト・時間が登録されているか。
  def test_object_list(self):
    self.assertQuerysetEqual(self.response_top.context['object_list'], ['<Post: test1>', '<Post: test2>'], ordered=False)
    self.response1 = self.response_top.context['object_list'][1]
    self.assertEqual(self.response1.name.username, 'kinoko')
    self.assertEqual(self.response1.text, 'test1')
    self.assertIsNotNone(self.response1.created_day)

  # deleteviewにpkを渡してきちんと削除できることの確認。また、削除した後それがhtml上から消えていることを確認。
  def test_tweet_delete(self):
    self.pk = self.response_top.context['object_list'][0].pk
    self.delete_url = reverse('blog:tweet-delete', args=[self.pk])
    self.response_delete = self.client.post(self.delete_url)
    self.response_top = self.client.get(self.top_url)    
    self.assertRedirects(self.response_delete, self.top_url, status_code=302, target_status_code=200)
    self.assertQuerysetEqual(self.response_top.context['object_list'], ['<Post: test1>'])
    self.assertContains(self.response_top, 'test1')
    self.assertNotContains(self.response_top, 'test2')
