from django import forms
from .models import Post

# Post라는 모델을 조작할 수 있는 PostForm 정의
class PostForm(forms.ModelForm):
   # 1. 어떤 input 필드를 가지는지
   content = forms.CharField(label="content", widget=forms.Textarea(attrs={
       'placeholder': '오늘은 무엇을 하셨나요?'
       }
   ))

   # 2. 해당 input 필드 속성을 추가 & 어떤 모델을 조작할지
   class Meta:
       model = Post
       fields = ['content']