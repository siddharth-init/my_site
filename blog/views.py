from datetime import date, datetime
from tokenize import Single
from turtle import pos
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect

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
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False

        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)

        context = {
            "post": post,
            "all_tags": post.tags.all(),
            "comments": post.comments.all().order_by("-id"),
            "comment_form": CommentForm(),
            "is_saved_for_later": self.is_stored_post(request, post.id),
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            "post": post,
            "all_tags": post.tags.all(),
            "comments": post.comments.all().order_by("-id"),
            "comment_form": CommentForm(),
            "is_saved_for_later": self.is_stored_post(request, post.id),
        }
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        return render(request, "blog/post-detail.html", context)


class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")
        context = {}
        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True
        return render(request, "blog/read-later.html", context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")
