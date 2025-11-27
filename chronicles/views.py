from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Post


def post_list(request):
    post_list = Post.published.all()
    # Pagination with 3 post per page.
    paginator = Paginator(post_list, 3)
    page_num = request.GET.get("page", 1)

    try:
        page_obj = paginator.page(page_num)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        page_obj = paginator.page(1)

    return render(request, "chronicles/post_list.html", {"posts": page_obj})


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=slug,
    )

    return render(request, "chronicles/post_detail.html", {"post": post})
