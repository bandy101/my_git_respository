from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown 

register = template.Library()

# 如果想使用其他的名称，可以通过name属性指定，
# 例如@register.simple_tag(name='my_tag')。
@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_comment_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).\
        order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_fomat(text):
    return mark_safe(markdown.markdown(text))