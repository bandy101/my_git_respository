from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

def post_list(request):
    # posts = Post.published.all()
    # return render(request, 'blog/post/list.html', {'posts': posts})

    # 使用django 自带分页
    object_list = Post.published.all()
    paginator = Paginator(object_list,2) # 每页显示三篇文章
    page = request.GET.get('page') # django自带分页参数
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 如果page参数非整数返回第一页
        posts  = paginator.page(1)
    except EmptyPage:
        # 如果超出总页数返回最后一页
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html',{'page':page,'posts':posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status="published", publish__year=year, publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})

from  django.views.generic import ListView
class PostListView(ListView):
    # Django内置的ListView返回的变量名称叫做page_obj 修改模板T
    # model = Post    # 可用queryset = Post.published.all() 替代
    queryset = Post.published.all()
    print (queryset)
    context_object_name='posts'    # 如果不设置context_object_name参数，默认的变量名称是object_list
    paginate_by = 2 # 每页的显示文章数
    template_name = 'blog/post/list.html'


from .forms import EmailPostForm
from django.core.mail import send_mail
def post_share(request,post_id):
    post = get_object_or_404(Post,id=post_id,status='published')
    sent = False
    if request.method=='POST':
        # 表单提交
        form = EmailPostForm(request.POST)
        if form.is_valid(): # 验证表单数据是否有效
    #   如果表单验证成功，可以通过form.cleaned_data属性访问表单内所有通过验证的数据，这个属性类似于一个字典，包含字段名与值构成的键值对。
    #   如果表单验证失败，form.cleaned_data只会包含通过验证的数据。
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, '1255381744@qq.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request,'blog/post/share.html',{'form':form,'post':post,'sent':sent})