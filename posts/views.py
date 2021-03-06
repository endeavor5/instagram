from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm
from .models import Post, Comment
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q


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
        
        
@login_required
def list(request):

    # 내가 쓴 포스트 - 포스트에서 뒤적거리지 말고 set으로 가져와
    my_posts = request.user.post_set.all()
    # 내가 팔로잉 하는 사람들 + 나의 게시물만 보여준다.
    followings = request.user.followings.all()
    posts = Post.objects.filter(Q(user_id__in=request.user.followings.all())|Q(user=request.user)).order_by('-id')
    
    print(posts.query)
    comment_form = CommentForm()
    return render(request, 'posts/list.html', {'posts':posts, 'comment_form':comment_form})


def update(request, post_id):
    # post = Post.objects.get(pk=post_id)
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


# Comment
@login_required
# @require_POST
def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        # comment의 유저 저장
        # foreignKey가 2개이기 때문에 각각의 객체를 넣어줘야한다.
        comment.user = request.user
        comment.post = post # 이것은 객체를 바로 넣어준 것
        # commnet.post_id = post_id # 얘는 아이디를 넣어준 것
        comment.save()
        
    return redirect('posts:list')


@login_required
@require_POST
def comment_delete(request, post_id, comment_id):
    # post = get_object_or_404(Post, pk=post_id)
    comment = Comment.objects.get(pk=comment_id)
    
    if comment.user == request.user:
        comment.delete()

    return redirect('posts:list')
    
