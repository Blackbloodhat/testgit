# -*- coding:utf-8 -*-
from django.contrib.auth.models import User
from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(
        label=u'昵称',
        help_text=u'昵称可用于登录，不能包含空格和@字符。',
        max_length=20,
        initial='',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        )

    email = forms.EmailField(
        label=u'邮箱',
        help_text=u'邮箱可用于登录，最重要的是需要邮箱来找回密码，所以请输入您的可用邮箱。',
        max_length=50,
        initial='',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        )

    password = forms.CharField(
        label=u'密码',
        help_text=u'密码只有长度要求，长度为 6 ~ 18 。',
        min_length=6,
        max_length=18,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        )

    confirm_password = forms.CharField(
        label=u'确认密码',
        min_length=6,
        max_length=18,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        if ' ' in username or '@' in username:
            raise forms.ValidationError(u'昵称中不能包含空格和@字符')
        res = User.objects.filter(username=username)
        if len(res) != 0:
            raise forms.ValidationError(u'此昵称已经注册，请重新输入')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        res = User.objects.filter(email=email)
        if len(res) != 0:
            raise forms.ValidationError(u'此邮箱已经注册，请重新输入')
        return email

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(u'两次密码输入不一致，请重新输入')

    def save(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = User.objects.create_user(username, email, password)
        user.save()


# class LoginForm(forms.Form):
#     '''
#     登录Form
#     '''
#     username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required", }),
#                                max_length=50, error_messages={"required": "username不能为空",})
#     password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required", }),
#                                max_length=20, error_messages={"required": "password不能为空",})


# class RegForm(forms.Form):
#     '''
#     注册表单
#     '''
#     username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required", }),
#                                max_length=50,error_messages={"required": "username不能为空",})
#     email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Email", "required": "required", }),
#                              max_length=50, error_messages={"required": "email不能为空",})
#     # url = forms.URLField(widget=forms.TextInput(attrs={"placeholder": "Url", }),
#     #                           max_length=100, required=False)
#     password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required", }),
#                                max_length=20, error_messages={"required": "password不能为空",})