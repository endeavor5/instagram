from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post
from django.views.decorators.http import require_POST

# Create your views here.
def create(request):
   if request.method=="POST":
       # 작성된 post를 DB에 적용
       form =PostForm(request.POST, request.FILES)
       if form.is_valid():
           form.save()
       return redirect('posts:list')
   else:
       # 새로 post 작성하는 form 페이지 보여줌
       form = PostForm()
       return render(request, 'posts/create.html', {'form':form})


def list(request):
   posts = Post.objects.all()
   return render(request, 'posts/list.html', {'posts':posts})
   

def update(request, id):
    # post = Post.objects.get(pk=id)
    # 해당하는 아이디가 없으면 에러페이지를 보여준다.
    post = get_object_or_404(Post, pk=id)
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
    post.delete()
    return redirect('posts:list')
    
    