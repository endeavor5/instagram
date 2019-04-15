from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

# Create your views here.

def login(request):
    # form을 쓰는 이유?
    # POST : 실제 로그인(세션에 유저 정보 추가)
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            # next가 정의 되어있으면 해당하는 url로 리다이렉트
            # 정의되어있지 않으면 posts:list로 돌아가셈
    
            return redirect(request.GET.get('next') or 'posts:list') 
    else: 
        # GET: 로그인 정보 입력
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form':form})
    


def logout(request):
    auth_logout(request)
    return redirect('posts:list')
    