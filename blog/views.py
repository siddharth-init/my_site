from datetime import date, datetime
from tokenize import Single
from turtle import pos
from django.shortcuts import render
from django.http import HttpResponse, Http404

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic import View

# from .data import blog_posts
from .models import Post
from .forms import CommentForm

# Create your views here.


class StartPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    """
    For using limit I am overriding the get_queryset method
    """

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


class AllPostsView(ListView):
    """
    Here I need not to override the get_context_data method, because
    The Auhor class has one to many relationship with Post, Not Many to many
    """

    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"


class SinglePostView(View):
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            "post": post,
            "all_tags": post.tags.all(),
            "comments": post.comments.all().order_by("-id"),
            "comment_form": CommentForm(),
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            "post": post,
            "all_tags": post.tags.all(),
            "comments": post.comments.all().order_by("-id"),
            "comment_form": CommentForm(),
        }
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        return render(request, "blog/post-detail.html", context)
