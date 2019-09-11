import hashlib

from django.shortcuts import render, HttpResponse, redirect, reverse

from crm import forms
from crm import models
from rbac.service.permission import init_permission


def login(request):
    err_msg = ''
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        en_pwd = hashlib.md5()
        en_pwd.update(pwd.encode('utf-8'))
        obj = models.UserProfile.objects.filter(username=user, password=en_pwd.hexdigest()).first()
        if obj:
            request.session['user_id'] = obj.pk
            init_permission(request, obj)
            return redirect('/index/')
        err_msg = '账号或密码错误！'
    return render(request, 'login.html', {'err_msg': err_msg})


def logout(request):
    del request.session['user_id']
    return redirect(reverse('login'))


def index(request):
    return HttpResponse('index')


def register(request):
    form_obj = forms.RegisterForm()
    if request.method == 'POST':

        form_obj = forms.RegisterForm(request.POST)
        if form_obj.is_valid():
            # 写到数据库
            form_obj.save()
            return redirect('/login/')
    return render(request, 'register.html', {'form_obj': form_obj})
