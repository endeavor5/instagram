from django.contrib.auth.forms import UserChangeForm, UserCreationForm
# 추천하지 않는 방식
from django.contrib.auth.models import User
# 추천 방식
# 1. settings.
# 2. get_user
from django.contrib.auth import get_user_model
from django import forms
from .models import Profile


#UserChangeForm을 조금 더 확장시킨 폼
class CustomUserChangeForm(UserChangeForm):
    # meta정보는 상속을 받더라도 명시적으로 써주는 것이 좋다.
    # 혹시나 우리가 다르게 정의한 유저가 있을 수도 있으니까... (그것은 auth user와 다름)
    class Meta:
        model = get_user_model()
        fields = ['username','email','first_name', 'last_name']    

    
class CustomUserCreationForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields


class ProfileForm(forms.ModelForm):        
    class Meta:
        model = Profile
        fields =['description', 'nickname', 'image'] 
        

