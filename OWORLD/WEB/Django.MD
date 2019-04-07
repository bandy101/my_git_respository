#   python manage.py migrate
    在数据库中创建INSTALLED_APPS中应用所需的数据表 (数据库迁移)
# setting INSTALLED_APPS 存放将要激活的应用
    BlogConfig类是我们应用的配置类。[Appconfig]
# python manage.py makemigrations blog  将为模型创建迁移数据 [检测你对模型文件的修改                                                models]
# python manage.py sqlmigrate blog 0001 了解Django实际执行的SQL语句预览

# from django.db import models  数据库与新的数据模型进行同步

# python manage.py createsuperuser 注册一个超级用户管理后台

# 查询数据
    每个模型都有至少一个管理器，默认的管理器叫做🌂objects。通过使用一个模型管理器，可以得到一个QuerySet，想得到一个数据表里的所有数据对象，可以使用默认模型管理器的all()方法

    Django ORM的全部使用都基于QuerySet（查询结果集对象，由于该术语使用频繁，因此在之后的文章中不再进行翻译）。一个查询结果集是一系列从数据库中取得的数据对象，经过一系列的过滤条件，最终组合到一起构成的一个对象。

    使用模型管理器的filter()过滤所需的数据 
        Post.objects.filter(publish__year=2017)，
        Post.objects.filter(publish__year=2017, author__username='admin')
        Post.objects.filter(publish__year=2017).filter(author__username='admin') 链式
        🔺QuerySet中使用的条件查询采用双下划线写法，比如例子中的            publish__year，双下划线还一个用法是从关联的模型中取其字段，例如author__username。
    使用模型管理器的exclude()从结果集中去除符合条件的数据
    选出2017年发布的所有标题不以     Why开头的文章：
        Post.objects.filter(publish__year=2017).exclude(title__startswith='Why')
    使用order_by()方法按照不同的字段进行排序 
    默认升序排列，如果需要使用降序排列，在字符串格式的字段名前加一个减号-
        order_by('-+xx')
    删除一个模型 
        post = Post.objects.get(id=1)
        post.delete()
    filter()，exclude()，all()这三个方法都返回一个QuerySet对象，所以可以任意链式调用。



# 视图
    {% static %} 模板标签会生成静态文件的绝对路径。
    {% extends %}，让该模板继承了母版blog/base.html
    {% block %}表示这个标签的开始与结束部分定义了一个块{% endblock %}
    truncatewords用来截断指定数量的文字，linebreaks将结果带上一个HTML换行

    
    template tags：进行渲染控制，类似{% tag %}
    template variables：可认为是模板标签的一种特殊形式，即只是一个变量，渲染的时候只替换内容，类似{{ variable }}
    template filters：附加在模板变量上改变变量最终显示结果，类似{{ variable|filter }}
        pluralize :表示复数

# Django的路由系统指的是路径和函数的对应关系
# Django 对于末尾没有/的路径,会自动加上”/”然后在用这个URL去匹配,如果想关闭该功能,需要在settings.py中加上 APPEND_SLASH=False 即可.默认是True

# Django自带分页器
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

    使用要分页的内容和每页展示的内容数量，实例化Paginator类得到paginator对象 paginator = Paginator(X.objects.all(),page)
    通过get()方法获取page变量，表示当前的页码
    调用paginator.page()方法获取要展示的数据
    如果page参数不是一个整数就返回第一页，如果页数超出总页数就返回最后一页 paginator.num_pages
    把页码和要展示的内容传给页面。
    返回变了名字 page_obj  {% include 'paginator.html' with page=page_obj %}
        with重新指定了变量名称以让分页模板
    
# 表单 
    Django默认会对所有POST请求进行CSRF检查，在所有POST方式提交的表单中，都要添加csrf_token。
    如果浏览器在提交根据表单的HTML元素属性先进行了验证，关闭浏览器验证的方法是给表单添加novalidate属性：<form action="" novalidate>
    {% with %}标签经常用于避免反复对数据库进行查询和向模板传入过多变量。

# 自定义标签
    simple_tag: 处理数据并且返回字符串
    inclusion_tag: 处理数据并返回一个渲染的模板

    Django对于生成的HTML代码都会进行转义而不会当成HTML代码解析，只有对mark_safe标记的内容才会正常解析，这是为了避免在页面中出现危险代码（如添加外部JavaScript文件的代码）。
    @register.filter(name='markdown')
    def markdown_format(text):
        return mark_safe(markdown.markdown(text))

# 站点地图
    在setting 中激活应用
        <!-- 'django.contrib.sites', -->
        'django.contrib.sitemaps',

# 全文搜索
    先安装postgreSQL和python 相关依赖项
    sudo apt-get install libpq-dev python-dev
    sudo apt-get install postgresql postgresql-contrib