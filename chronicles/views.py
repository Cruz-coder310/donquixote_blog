from django.shortcuts import get_object_or_404, render

from .models import Post


def post_list(request):
    posts = Post.published.all()
    return render(request, "chronicles/post_list.html", {"posts": posts})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLISHED)

    return render(request, "chronicles/post_detail.html", {"post": post})
