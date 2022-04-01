from django.test import TestCase
from django.urls import resolve
from ..views import TopView, TweetView, TweetDelete

class UrlTests(TestCase):
  def test_top_url(self):
    view = resolve('/blog/')
    self.assertEqual(view.func.view_class, TopView)

  def test_tweet_url(self):
    view = resolve('/blog/tweet/')
    self.assertEqual(view.func.view_class, TweetView)
