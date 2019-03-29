from django import forms

# 邮件的功能里，采用继承forms.Form类的方式，自行编写各个字段创建了一个表单。
# Django对于表单有两个类：Form和ModelForm。
# 这次我们使用ModelForm动态的根据Comment模型生成表单


#save()方法仅对ModelForm生效，因为Form类没有关联到任何数据模型。
class EmailPostForm(forms.Form):
    # 每个字段都有一个默认的widget参数决定该字段被渲染成的HTML元素类型
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    # required=False表示该字段可以没有任何值
    comments = forms.CharField(required=False, widget=forms.Textarea)

from .models import Comment

class CommentForm(forms.ModelForm):
    
    # 依据模型创建表单，只需要在Meta类中指定基于哪个类即可。
    # Django会自动内省该类然后创建对应的表单。
    # 可以显示的通过Meta类中的fields属性指定需要创建表单元素的字段
    class Meta:
        model = Comment
        # fields = '__all__'
        fields  = ('name','email','body')