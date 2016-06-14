# coding:utf-8
from django.conf.urls import url
from .import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^article/(?P<blog_body_id>[0-9]+)/$', views.article, name='article'),
    url(r'^python/$', views.python,name='python'),
    url(r'^add_article/', views.add_article, name='add_article'),
    url(r'^del_article/(?P<blog_body_id>\d+)/$', views.del_article, name='del_article'),
    url(r'^logout/$', views.do_logout, name='logout'),
    # url(r'^login/', views.do_login, name='login'),
    # url(r'^reg/', views.do_reg, name='reg'),
    url(r'^login/$', views.account_login, name='login'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^yes/$', views.yes, name='yes'),
]
