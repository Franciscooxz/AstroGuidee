from django.shortcuts import render, get_object_or_404
from .models import Post, BlogCategory


def post_list(request):
    category_slug = request.GET.get('cat')
    posts = Post.objects.filter(is_published=True)
    categories = BlogCategory.objects.all()
    active_category = None
    if category_slug:
        active_category = get_object_or_404(BlogCategory, slug=category_slug)
        posts = posts.filter(category=active_category)
    return render(request, 'blog/list.html', {
        'posts': posts,
        'categories': categories,
        'active_category': active_category,
        'active_nav': 'blog',
    })


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    recent = Post.objects.filter(is_published=True).exclude(pk=post.pk).order_by('-published_at')[:3]
    return render(request, 'blog/detail.html', {
        'post': post,
        'recent_posts': recent,
        'active_nav': 'blog',
    })
