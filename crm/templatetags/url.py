#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'whj'
# Date: 2019/3/9 15:13
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
    params = request.GET.urlencode()
    if not params:
        return base_url
    return '{}?{}'.format(base_url, params)


@register.simple_tag()
def rev_url(request, name, *args, **kwargs):
    """
    反向解析生成URL，拼接参数
    :return:
    """

    base_url = reverse(name, args=args, kwargs=kwargs)

    # 直接拿到当前的URL
    url = request.get_full_path()
    qd = QueryDict(mutable=True)
    qd['next'] = url
    return "{}?{}".format(base_url, qd.urlencode())
