from django.forms import ModelForm, TextInput
from django.forms.widgets import Textarea
from .models import Post

class TweetForm(ModelForm):
    class Meta:
        model = Post
        fields = ('text',)
        widgets = {
            'text':Textarea(attrs={'rows':'10', 'placeholder':'200文字以内で入力してください'}),
        }
