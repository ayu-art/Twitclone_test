from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from .form import TweetForm
from .models import Post

class TopView(ListView):
  model = Post
  template_name = 'blog/top.html'
  paginate_by = 20

  def get_queryset(self):
    return Post.objects.order_by('-created_day')


class TweetView(CreateView, LoginRequiredMixin):
  form_class = TweetForm
  template_name = 'blog/tweet.html'
  success_url = reverse_lazy('blog:top')

  def form_valid(self, form):
    form.instance.name = self.request.user
    return super().form_valid(form)

  def form_invalid(self, form):
    return render(self.request, 'blog/tweet.html', {'form': form})


class TweetDelete(DeleteView):
  template_name = None
  model = Post
  success_url = reverse_lazy('blog:top')
