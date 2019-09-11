#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import reverse


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


def rev_url(request, name, *args, **kwargs):
    # 完成操作后可以调回原页面
    base_url = reverse(name, args=args, kwargs=kwargs)
    next_url = request.GET.get('next')
    if next_url:
        return next_url
    return base_url
