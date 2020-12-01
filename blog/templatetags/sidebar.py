from django import template
from blog.models import Post, Category

register = template.Library()


@register.inclusion_tag('popular_posts_tpl.html')
def get_popular(cnt=3):
    posts = Post.objects.order_by('-views')[:cnt]
    return {"posts": posts}


@register.inclusion_tag('categories_posts_tpl.html')
def get_cat():
    categories = Category.objects.all()
    return {"categories": categories}


@register.inclusion_tag('tags_posts_tpl.html')
def get_tag():
    tags = Category.objects.all()
    return {"tags": tags}
