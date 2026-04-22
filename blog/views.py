from datetime import date, datetime
from django.shortcuts import render
from django.http import HttpResponse
from .data import blog_posts


# Create your views here.
def starting_page(request):
    # sorted_posts = sorted(blog_posts, key=lambda post: post["date"], reverse=True)
    # latest_posts = sorted_posts[-3:]
    # print(len(latest_posts))
    return render(request, "blog/index.html", {"posts": blog_posts})


def posts(request):
    return render(request, "blog/all-posts.html", {"posts": blog_posts})


def post_detail(request, slug):
    identified_posts = next(post for post in blog_posts if post["slug"] == slug)
    return render(request, "blog/post-detail.html", {"post": identified_posts})
