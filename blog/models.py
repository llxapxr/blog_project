# -*- coding:utf-8 -*-
from django.db import models, connection


# Create your models here.
class category(models.Model):
    category_name = models.CharField(max_length=30, verbose_name='类别名')

    class Meta:
        verbose_name = '分类表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


class user(models.Model):
    username = models.CharField(max_length=30, verbose_name='用户名')
    password = models.CharField(max_length=32, verbose_name='密码')
    email = models.CharField(max_length=50, null=True, blank=True, verbose_name='邮箱')
    ID_number = models.CharField(max_length=18, null=True, blank=True, verbose_name='身份证号')
    real_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='真实姓名')
    age = models.IntegerField(null=True, blank=True, verbose_name='年龄')
    user_head = models.CharField(null=True, blank=True, max_length=255, verbose_name='用户头像')
    introduce = models.CharField(max_length=255, default='', blank=True, null=True)
    type = models.IntegerField(null=True, blank=True, verbose_name='用户分类')

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


class company(models.Model):
    company_name = models.CharField(max_length=30, verbose_name='公司名称')
    company_head = models.CharField(null=True, blank=True, max_length=255, verbose_name='公司标志')
    company_introduce = models.CharField(null=True, blank=True, max_length=255, verbose_name='公司简介')

    class Meta:
        verbose_name = '公司信息表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


class complaint(models.Model):
    brand_id = models.ForeignKey(company, on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(user, related_name='user_complaint', on_delete=models.DO_NOTHING)
    product = models.CharField(null=True, blank=True, max_length=50, verbose_name='产品')
    title = models.CharField(max_length=50, verbose_name='标题')
    content = models.CharField(max_length=8000, verbose_name='内容')
    category_id = models.ForeignKey(category, on_delete=models.DO_NOTHING)
    reply_amount = models.IntegerField(null=True, blank=True, verbose_name='浏览量')
    pic = models.CharField(null=True, blank=True, max_length=255, verbose_name='投诉图片')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    status = models.IntegerField(null=True, blank=True, verbose_name='状态')

    class Meta:
        verbose_name = '投诉表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


class comment(models.Model):
    content = models.TextField(max_length=8000, verbose_name='内容')
    user_id = models.ForeignKey(user, on_delete=models.DO_NOTHING)
    complaint_id = models.ForeignKey(complaint, on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '评论表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


class red_black(models.Model):
    company_id = models.ForeignKey(company, on_delete=models.DO_NOTHING)
    score = models.IntegerField(verbose_name='群众打分')
    complaint_amount = models.IntegerField(null=True, blank=True, verbose_name='投诉数量')
    is_red = models.BooleanField(default=False, verbose_name='是否在红榜')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '红黑榜'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


class news(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    news_introduce = models.CharField(max_length=255, verbose_name='大致描述')
    content = models.TextField(max_length=8000, verbose_name='内容')
    pic = models.CharField(null=True, blank=True, max_length=255, verbose_name='新闻图片')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '新闻'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


class latest_complaint(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    complaint_id = models.ForeignKey(complaint, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = '最近发帖'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


class hot_complaint(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    complaint_id = models.ForeignKey(complaint, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = '热门帖'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


class hot_news(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    news_id = models.ForeignKey(news, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = '热门新闻'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


class collection_user(models.Model):
    user_id = models.ForeignKey(user, on_delete=models.DO_NOTHING, related_name='uid')
    collected_user_id = models.ForeignKey(user, on_delete=models.DO_NOTHING,
                                          related_name='collected_uid')

    class Meta:
        verbose_name = '关注的用户'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


class collection_complaint(models.Model):
    user_id = models.ForeignKey(user, on_delete=models.DO_NOTHING)
    collected_complaint_id = models.ForeignKey(complaint, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = '关注的帖子'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)
