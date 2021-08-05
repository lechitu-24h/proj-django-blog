from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth_login(request, user)
            return redirect('post_list')
        else:
            return render(request, 'blog/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'blog/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('login')


def post_list(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(
            published_date__lte=timezone.now()).order_by('published_date')
        return render(request, 'blog/post_list.html', {'posts': posts})
    else:
        return redirect('login')


def post_detail(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'blog/post_detail.html', {'post': post})
    else:
        return redirect('login')


def post_new(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            print(form)
            print(form.is_valid())
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})
    else:
        return redirect('login')


def post_edit(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})
    else:
        return redirect('login')
