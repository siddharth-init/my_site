from datetime import date, datetime
from tokenize import Single
from turtle import pos
from django.shortcuts import render
from django.http import HttpResponse, Http404

from django.views.generic import ListView
from django.views.generic.detail import DetailView

# from .data import blog_posts
from .models import Post

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


class SinglePostView(DetailView):
    template_name = "blog/post-detail.html"
    model = Post

    """
    For using the Tag class I am overriding the get_context_data to get all tags
    It has many to many relationship with Posts
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_tags"] = self.object.tags.all()  # type: ignore
        return context
