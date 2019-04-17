from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
# 로그인: AuthenticationForm, 회원가입: UserCreationForm
from django.contrib.auth import get_user_model, update_session_auth_hash
from .forms import CustomUserChangeForm, ProfileForm
from .models import Profile

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
            Profile.objects.create(user=user)
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
    

# 회원 정보 변경 - 편집 + 반영
# post를 업데이트하는 것과 동일하다.
def update(request):
    if request.method == "POST":
        user_change_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm(data=request.POST, instance=request.user.profile) # 어떤 프로필인지 정확하게 골라내지 못한다.
        
        # profile_form = ProfileForm(request.POST, instance=request.user.profile) # 어떤 프로필인지 정확하게 골라내지 못한다.
        if user_change_form.is_valid() and profile_form.is_valid(): 
            # 객체를 돌려줌
            user = user_change_form.save()
            profile_form.save()
            return redirect('people', user.username)
            
    else:
        # form이 여러개이니까 이제는 명확하게 쓰자   
        # post의 경우 instance 값으로 
        # 현재 로그인된 유저의 정보를 넘겨주자.
        
        # user_change_form을 그대로 가져오면 위험스
        user_change_form = CustomUserChangeForm(instance=request.user)
        
        # instance에 넣어줄 정보가 있는 user가 있고 없는 user도 있다.

        profile, created = Profile.objects.get_or_create(user=request.user)
        profile_form = ProfileForm(instance=profile)
            
        #     profile_form = ProfileForm(instance=request.user)
        # profile_form = ProfileForm(instance=request.user)
        
        # Profile.get_or_create(user=requeset.user)
        
        context = {
            'user_change_form': user_change_form,
            'profile_form': profile_form,
        }
        return render(request, 'accounts/update.html', context)
    
        
def delete(request):
    # 내가 본인일 때만 탈퇴하도록
    if request.method == "POST":
        request.user.delete()
        return redirect('accounts:signup')
        
    return render(request, 'accounts/delete.html')
    

def password(request):
    if request.method == "POST":
        password_change_form = PasswordChangeForm(request.user, request.POST)
        # 다시 로그인해야되는 번거로움을 피하기 위해 update_session()을 사용하자
        if password_change_form.is_valid():
            # user = password_change_form.save()
            update_session_auth_hash(request, password_change_form)
        return redirect('people', request.user)
            
    else:
        password_change_form = PasswordChangeForm(request.user)
        return render(request, 'accounts/password.html', {'password_change_form':password_change_form})