from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post
import markdown 
from django.utils.safestring import mark_safe


#item_description(self, item)这个函数并没有对post.body进行处理，所以会返回未经处理的markdown代码，
#在不支持markdown的Feed阅读器里会出现问题，读者可以修改该函数，调用markdown库输出转换后的字符串。
class LastestPostFeed(Feed):
    title = 'My blog'
    link = '/blog/'
    description = 'New posts of my blog.'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        value = (markdown.markdown(item.body))
        return truncatewords(value, 30)