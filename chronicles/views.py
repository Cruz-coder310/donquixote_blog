# Django Core
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.core.mail import send_mail
from django.views.decorators.http import require_POST

# Third-Party package
from taggit.models import Tag

# Local apps impots
from .forms import EmailPostForm, CommentForm
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
    comments = post.comments.filter(active=True)

    form = CommentForm()

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
            "comments": comments,
            "form": form,
        },
    )


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post.published, id=post_id)
    comment = None

    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return render(
        request,
        "chronicles/post_comment.html",
        {
            "post": post,
            "comment": comment,
            "form": form,
        },
    )


def post_share(request, post_id):
    post = get_object_or_404(Post.published, id=post_id)
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} te recomienda: {post.title}"

            message = (
                f"Hola,\n\n"
                f"{cd['name']} ({cd['email']}) quiere compartir contigo este post:\n"
                f"{post.title}\n{post_url}\n\n"
                f"Comentarios:\n{cd['comments']}\n\n"
                "Saludos,"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd["to"]],
            )
            sent = True

    else:
        form = EmailPostForm()

    return render(
        request,
        "chronicles/post_share.html",
        {
            "form": form,
            "post": post,
            "sent": sent,
        },
    )
