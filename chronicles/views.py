from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count

from taggit.models import Tag

from .models import Post


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    # Pagination with 3 post per page.
    paginator = Paginator(post_list, 3)
    page_num = request.GET.get("page", 1)

    try:
        page_obj = paginator.page(page_num)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        page_obj = paginator.page(1)

    return render(
        request,
        "chronicles/post_list.html",
        {
            "posts": page_obj,
            "tag": tag,
        },
    )


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=slug,
    )
    # List of similar post
    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )[:4]

    return render(
        request,
        "chronicles/post_detail.html",
        {
            "post": post,
            "similar_posts": similar_posts,
        },
    )
