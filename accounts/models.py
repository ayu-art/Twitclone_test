from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
  email = models.EmailField(_('email address'), blank=False, unique=True)
  introduce_text = models.CharField(verbose_name='自己紹介', max_length=200, help_text='簡単な自己紹介を200文字以内で書いてください。', blank=True, null=False,)
  place = models.CharField(verbose_name='住んでいる場所', max_length=50, help_text='50文字以内です', blank=True, null=False)
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  def __str__(self):
    return self.email
