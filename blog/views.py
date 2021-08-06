from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django import forms


def login(request):
    if request.method == "POST":
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth_login(request, user)
            return redirect('post_list')
    return render(request, 'blog/login.html')


def logout(request):
    auth_logout(request)
    return redirect('login')


def post_list(request):
    if request.user.is_authenticated:
        search = [
            {
                'title': 'Title',
                'value': 'title'
            },
            {
                'title': 'Content',
                'value': 'text'
            }
        ]

        if request.method == "POST" and request.POST['searchText']:
            searchText = request.POST['searchText']
            searchWith = request.POST['searchWith']
            posts = Post.objects.filter(
                published_date__lte=timezone.now()).order_by('published_date')
            if searchWith == "text":
                posts = posts.filter(text__contains=searchText)
            else:
                posts = posts.filter(title__contains=searchText)
            return render(request, 'blog/post_list.html', {'posts': posts, 'searchText': searchText, 'search': search, 'searchWith': searchWith})
        else:
            posts = Post.objects.filter(
                published_date__lte=timezone.now()).order_by('published_date')
            return render(request, 'blog/post_list.html', {'posts': posts, 'search': search})
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


def post_delete(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect('post_list')
    else:
        return redirect('login')
