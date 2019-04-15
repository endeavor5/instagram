from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# Create your views here.
def create(request):
   if request.method=="POST":
       # 작성된 post를 DB에 적용
       form =PostForm(request.POST, request.FILES)
       if form.is_valid():
           post = form.save(commit=False)
           post.user = request.user
           post.save()
           # form.save()
       return redirect('posts:list')
   else:
       # 새로 post 작성하는 form 페이지 보여줌
       form = PostForm()
       return render(request, 'posts/create.html', {'form':form})
        

def list(request):
   posts = Post.objects.all()
   return render(request, 'posts/list.html', {'posts':posts})
   

def update(request, post_id):
    # post = Post.objects.get(pk=id)
    # 해당하는 아이디가 없으면 에러페이지를 보여준다.
    post = get_object_or_404(Post, pk=post_id)
    
    if post.user != request.user:
        return redirect('posts:list')
    
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:list')
    else:
        # 수정페이지
        form = PostForm(instance=post)
        return render(request, 'posts/update.html', {'form':form})
        
        
@require_POST
def delete(request, id):
    post = Post.objects.get(pk=id)
    if post.user != request.user:
        return redirect('posts:list')
    post.delete()
    return redirect('posts:list')


@login_required
def like(request, post_id):
    # 1. like를 추가할 post를 가져옴
    post = get_object_or_404(Post, pk=post_id)
    # post = Post.objects.get(id=id)
    # 2. 만약 유저가 해당 post를 이미 like 했다면, like를 제거하고
    #    아니라면 like를 추가한다.
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
    else:
        post.like_users.add(request.user)
    return redirect('posts:list')
