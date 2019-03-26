from django import forms

class EmailPostForm(forms.Form):
    # 每个字段都有一个默认的widget参数决定该字段被渲染成的HTML元素类型
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    # required=False表示该字段可以没有任何值
    comments = forms.CharField(required=False, widget=forms.Textarea)