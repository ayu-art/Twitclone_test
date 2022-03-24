from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from .form import TweetForm
from .models import Post

class TopView(ListView):
  model = Post
  template_name = 'blog/top.html'
  paginate_by = 20

  def get_queryset(self):
    return Post.objects.order_by('-created_at')


class OnlyYouMixin(UserPassesTestMixin):
  raise_exception = True

  def test_func(self):
    tweet = get_object_or_404(Post, pk=self.kwargs['pk'])
    return self.request.user == tweet.name


class TweetView(LoginRequiredMixin, CreateView):
  form_class = TweetForm
  template_name = 'blog/tweet.html'
  success_url = reverse_lazy('blog:top')

  def form_valid(self, form):
    form.instance.name = self.request.user
    return super().form_valid(form)


class TweetDelete(LoginRequiredMixin, OnlyYouMixin, DeleteView):
  model = Post
  success_url = reverse_lazy('blog:top')
