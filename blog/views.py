from django.shortcuts import render
from django.utils import timezone
from .models import Post, Categories
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
        categories = Categories.objects.all()
        posts = Post.objects.filter(
            published_date__lte=timezone.now()).order_by('published_date')

        if request.method == "POST":
            category = request.POST['category']
            if category != 'all':
                category = int(category)
                posts = posts.filter(category=category)
            if request.POST['searchText']:
                searchText = request.POST['searchText']
                searchWith = request.POST['searchWith']

                if searchWith == "text":
                    posts = posts.filter(text__contains=searchText)
                else:
                    posts = posts.filter(title__contains=searchText)
                return render(request, 'blog/post_list.html', {'posts': posts, 'searchText': searchText, 'search': search, 'searchWith': searchWith, 'categories': categories, 'categoryId': category})
            return render(request, 'blog/post_list.html', {'posts': posts, 'search': search, 'categories': categories, 'categoryId': category})
        else:
            return render(request, 'blog/post_list.html', {'posts': posts, 'search': search, 'categories': categories})
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
        categories = Categories.objects.all()
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.category = get_object_or_404(
                    Categories, pk=request.POST['category'])
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form, 'categories': categories})
    else:
        return redirect('login')


def post_edit(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        categories = Categories.objects.all()
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.category = get_object_or_404(
                    Categories, pk=request.POST['category'])
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form, 'categories': categories, "categoryId": post.category.id})
    else:
        return redirect('login')


def post_delete(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect('post_list')
    else:
        return redirect('login')


def category_new(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            title = request.POST['category']
            category = Categories()
            category.text = title
            category.published_date = timezone.now()
            category.save()
            return redirect('post_list')
        return render(request, 'categories/category_edit.html')
    else:
        return redirect('login')
