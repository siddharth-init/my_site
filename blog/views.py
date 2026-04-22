from datetime import date, datetime
from django.shortcuts import render
from django.http import HttpResponse, Http404

# from .data import blog_posts
from .models import Post


# Create your views here.
def starting_page(request):
    all_posts = Post.objects.all().order_by("-date")[:3]
    return render(request, "blog/index.html", {"posts": all_posts})


def posts(request):
    blog_posts = Post.objects.all().order_by("-date")
    return render(request, "blog/all-posts.html", {"posts": blog_posts})


def post_detail(request, slug):
    try:
        single_post = Post.objects.get(slug=slug)
        all_tags = single_post.tags.all()
    except Post.DoesNotExist:
        raise Http404("Post does not exist")

    return render(
        request, "blog/post-detail.html", {"post": single_post, "all_tags": all_tags}
    )
