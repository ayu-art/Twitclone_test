from django.db import models
from accounts.models import User
from django.utils import timezone

class Post(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200, blank=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
