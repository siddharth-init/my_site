from django.urls import path
from . import views

urlpatterns = [
    path("", views.StartPageView.as_view(), name="starting_page"),
    path("posts/", views.AllPostsView.as_view(), name="all-posts"),
    path("posts/<slug:slug>", views.SinglePostView.as_view(), name="post_detail_page"),
]
