from django import forms
from django.contrib.auth.models import User
from .models import Profile, Comment


class UserEditForm(forms.ModelForm):  # 这个表单依据User类生成，让用户输入姓，名和电子邮件
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):  # 这个表单依据Profile类生成，可以让用户输入生日和上传一个头像
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')


class UserRegistrationForm(forms.ModelForm):  # 创建注册表单
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError(r"Password don't match.")
        return cd['password2']


class LoginForm(forms.Form):  # 创建登陆表单
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)  # 一般密码框不会明文显示，这里采用了widget=...，在页面上显示为一个输入密码的INPUT元素


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('username', 'email', 'body')

