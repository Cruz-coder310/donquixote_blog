from django.urls import path
from . import views
from .feeds import PostFeed

app_name = "chronicles"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:slug>/",
        views.post_detail,
        name="post_detail",
    ),
    path("tag/<slug:tag_slug>/", views.post_list, name="post_list_by_tag"),
    path("<int:post_id>/share/", views.post_share, name="post_share"),
    path("<int:post_id>/comment/", views.post_comment, name="post_comment"),
    path("edit-post/<int:post_id>/", views.edit_or_create_post, name="edit_post"),
    path("create-post/", views.edit_or_create_post, name="create_post"),
    path("feed/", PostFeed(), name="post_feed"),
]
