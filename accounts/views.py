from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# 로그인: AuthenticationForm, 회원가입: UserCreationForm
from django.contrib.auth import get_user_model
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
    

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            # user로 뽑는 이유? 결과물을 가지고 바로 로그인 해주려고
            user = form.save()
            # 회원가입이 끝나면 바로 로그인 해주기
            auth_login(request, user)
            return redirect('posts:list')
    else:
        form = UserCreationForm()
        return render(request, 'accounts/signup.html', {'form':form} )
        
        
def people(request, username):
    # 사용자에 대한 정보
    # 1. settings.AUTH_USER_MODEL => django.conf
    # 2. get_user_model()
    # 3. User => django.contrib.auth.models 안쓰는 것이 좋다....
    people = get_object_or_404(get_user_model(), username=username)
    return render(request, 'accounts/people.html', {'people':people} )