# coding:utf-8
from django.shortcuts import render, HttpResponseRedirect
from app.models import BlogBody, UserInfo
from django.shortcuts import redirect
import time
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.db import connection
from forms import *
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
# Create your views here.


def index(request):
    userinfo = UserInfo.objects.first()
    blog_body = BlogBody.objects.all()[:6]
    return render(request, 'index.html', {'userinfo': userinfo, 'blog_body':blog_body})


@login_required
def article(request, blog_body_id=''):
    blog_content = BlogBody.objects.get(id=blog_body_id)
    num = blog_content.blog_clicknum             # 点击量
    num += 1
    blog_content.blog_clicknum = num
    blog_content.save()
    return render(request, 'view.html', {'blog_content': blog_content})


@login_required
def python(request):
    sql = 'select id,blog_title,blog_type,blog_timestamp,blog_body from grzx_blogbody WHERE blog_type = "Python"'
    python_blog = BlogBody.objects.raw(sql)

    return render(request, 'python_list.html', {'python_blog': python_blog})


@login_required
def add_article(request):
    if request.method == "POST":
        article_title = request.POST['article_title']
        article_type = request.POST['article_type']
        article_content = request.POST['article_content']
        article_istop = request.POST['is_top']
        article_author = request.POST['article_author']
        print (article_title, article_type, article_content, article_istop,article_author)
        isdb = BlogBody(blog_title=article_title,
                        blog_body=article_content,
                        blog_type=article_type,
                        blog_timestamp=time.strftime("%Y-%m-%d %X", time.localtime()),
                        blog_author=article_author,
                        blog_clicknum=1,)
        isdb.save()
        return render(request, 'add_article.html')

    return render(request, 'add_article.html')


@login_required
def del_article(request, blog_body_id):
    BlogBody.objects.get(id=blog_body_id).delete()
    return redirect('/app/')


@login_required
def edit_article(request):
    pass

# 退出


def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        print e
    return redirect(request.META['HTTP_REFERER'])


def yes(request):
    return render(request, 'yes.html')


# 注册
class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('yes')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(RegisterView, self).form_valid(form)





#
# def do_reg(request):
#     try:
#         if request.method == 'POST':
#             reg_form = RegForm(request.POST)
#             if reg_form.is_valid():
#                 user = UserInfo.objects.create(username=reg_form.cleaned_date["username"],
#                                                email=reg_form.cleaned_data["email"],
#                                                # url=reg_form.cleaned_data['url'],
#                                                password=make_password(reg_form.cleaned_data["password"]),)
#                 user.save()
#                 # 登录
#                 user.backend = "django.contrib.auth.backends.ModelBackend"  # 默认指定的登录验证方式
#                 login(request, user)
#                 return redirect(request.POST.get('source_url'))
#             else:
#                 return render(request, 'failure.html', {'reason': reg_form.arrors})
#
#         else:
#             reg_form = RegForm()
#
#     except Exception as e:
#         print e
#     return render(request, "reg.html", locals())

# 登录

def account_login(request):

    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        print request.POST
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            user.userinfo.online = True
            user.userinfo.save()
            return HttpResponseRedirect("/app/")
        else:
            return render(request, 'login.html', {
                'login_err': 'Wrong username or password!'
            })

