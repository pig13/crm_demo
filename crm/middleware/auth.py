#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, reverse
from crm.models import UserProfile


class AuthAccount(MiddlewareMixin):
    def process_request(self, request):
        if request.path_info.startswith('/admin'):
            return

        if request.path_info == reverse('login'):
            return
        if request.path_info == reverse('register'):
            return

        pk = request.session.get('user_id')
        user = UserProfile.objects.filter(pk=pk).first()
        if user:
            request.account = user
        else:
            return redirect(reverse('login'))
