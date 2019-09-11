#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import template
from django.urls import reverse
from django.http import QueryDict

register = template.Library()


@register.simple_tag()
def revers_url(request, name, *args, **kwargs):
    """
    反向解析生成URL，拼接参数
    :param request:
    :param name:
    :param args:
    :param kwargs:
    :return:
    """
    base_url = reverse(name, args=args, kwargs=kwargs)
    params = request.GET.urlencode()  # 传递当前页面的查询参数给下一页面
    if not params:
        return base_url
    return '{}?{}'.format(base_url, params)


@register.simple_tag()
def rev_url(request, name, *args, **kwargs):
    """
    反向解析生成URL，拼接参数，与后端结合完成操作后可以调回原页面
    :return:
    """

    base_url = reverse(name, args=args, kwargs=kwargs)

    # 直接拿到当前的URL
    url = request.get_full_path()
    qd = QueryDict(mutable=True)
    qd['next'] = url
    return "{}?{}".format(base_url, qd.urlencode())
