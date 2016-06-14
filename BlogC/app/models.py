# coding:utf-8
from __future__ import unicode_literals
from django.contrib import admin
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
# Create your models here.


class BlogBody(models.Model):
    blog_title = models.CharField(max_length=50)
    blog_body = models.TextField()
    blog_type = models.CharField(max_length=50)
    blog_timestamp = models.DateTimeField()
    blog_imgurl = models.CharField(max_length=50, null=True, blank=True)
    blog_author = models.CharField(max_length=20,null=True)
    blog_ismarkdown = models.CharField(max_length=1, null=True)
    blog_like = models.IntegerField(null=True)
    blog_clicknum = models.IntegerField(null=True)

    def get_absolute_url(self):
        path = reverse('detail', kwargs={'id': self.id})
        return "http://127.0.0.1:8000%s" % path

    class Meta:
        ordering = ['-blog_timestamp']


class UserInfo(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=20)
    work = models.CharField(max_length=20)
    company = models.CharField(max_length=50)
    email = models.CharField(max_length=20, blank=True, null=True)

    def __unicode__(self):
        return self.nickname


admin.site.register(BlogBody)
admin.site.register(UserInfo)

