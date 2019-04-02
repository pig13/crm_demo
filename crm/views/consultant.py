from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views import View

from crm import forms
from crm import models
from crm.utils.pagination import Pagination
from crm.utils.url import revers_url


# 客户展示
def customer_list(request):
    if request.path_info == reverse('customer_list'):
        all_customer = models.Customer.objects.filter(consultant__isnull=True)
    else:
        all_customer = models.Customer.objects.filter(consultant=request.account)

    return render(request, 'consultant/customer_list.html', {'all_customer': all_customer})


class CustomerList(View):
    def get(self, request):
        q = self.search(['qq', 'name', 'date'])
        if request.path_info == reverse('customer_list'):

            all_customer = models.Customer.objects.filter(q, consultant__isnull=True)
        else:
            all_customer = models.Customer.objects.filter(q, consultant=request.account)

        pager = Pagination(request.GET.get('page', '1'), len(all_customer), params=request.GET.copy(), per_num=10,
                           max_show=15)

        return render(request, 'consultant/customer_list.html', {
            'all_customer': all_customer[pager.start:pager.end],
            'page_html': pager.page_html,
        })

    def post(self, request):
        res = None
        if hasattr(self, request.POST.get('action')):
            res = getattr(self, request.POST.get('action'))()
        # 如果没有抢到
        if res:
            return res
        return redirect(reverse('customer_list'))

    def multi_apply(self):
        """
        申请为私户
        :return:
        """
        pk = self.request.POST.getlist('pk')

        # 限制每个用户的最多客户数量
        if self.request.account.customers.all().count() + len(pk) > settings.MAX_ACCOUNT_NUM:
            return HttpResponse('已达拥有客户上限，无法再申请！')

        with transaction.atomic():
            # 查询出数据加锁
            query_set = models.Customer.objects.filter(pk__in=pk, consultant__isnull=True).select_for_update()  # 加锁
            # 如果没有抢到
            if len(pk) != len(query_set):
                return HttpResponse('手慢了，没抢到哦!')
            query_set.update(consultant=self.request.account)

    def multi_public(self):
        pk = self.request.POST.getlist('pk')
        models.Customer.objects.filter(pk__in=pk).update(consultant=None)

    def multi_delete(self):
        pk = self.request.POST.getlist('pk')
        models.Customer.objects.filter(pk__in=pk).delete()

    def search(self, query_list):
        query = self.request.GET.get('query', '')
        q = Q()
        q.connector = 'OR'
        # Q(qq__contains=query)   <==>   Q(('qq__contains',query))
        for i in query_list:
            q.children.append(Q(('{}__contains'.format(i), query)))
        return q


# 自定义的数据，由于数据库中暂时没有数据
all_user = [{'name': 'haha-{}号'.format(i), 'age': '{}岁'.format(i)} for i in range(407)]


# 用户展示
def user(request):
    page = request.GET.get('page', '1')
    try:
        page = int(page)
        if page < 1:
            page = 1
    except Exception as e:
        page = 1
    # 每页显示的数据条数
    per_num = 12
    # 总数据量
    all_count = len(all_user)
    # 总页码数
    page_num, more = divmod(all_count, per_num)
    if more:
        page_num += 1
    # 第X页第一个客户index
    start = (page - 1) * per_num
    # 第X页最后一个客户index
    end = page * per_num

    # 最多显示页码数
    max_show = 11
    half_show = max_show // 2
    if page_num < max_show:
        # 总页码数不够 最大显示页码数
        page_start = 1
        page_end = page_num
    else:
        # 能显示超过最大显示页码数
        if page <= half_show:
            # 处理左边的极值
            page_start = 1
            page_end = max_show
        elif page + half_show > page_num:
            # 处理右边的极值
            page_start = page_num - max_show + 1
            page_end = page_num
        else:
            # 正常的情况
            page_start = page - half_show
            page_end = page + half_show

    li_list = []
    if page == 1:
        li_list.append('<li class="disabled" ><a> << </a></li>')
    else:
        li_list.append('<li ><a href="?page={}"> << </a></li>'.format(page - 1))

    for i in range(page_start, page_end + 1):
        if page == i:
            li_list.append('<li class="active"><a href="?page={}">{}</a></li>'.format(i, i))
        else:
            li_list.append('<li><a href="?page={}">{}</a></li>'.format(i, i))
    if page == page_num:
        li_list.append('<li class="disabled" ><a> >> </a></li>')
    else:
        li_list.append('<li ><a href="?page={}"> >> </a></li>'.format(page + 1))
    page_html = ''.join(li_list)
    return render(request, 'consultant/user.html', {
        'all_user': all_user[start:end],
        'page_html': page_html,
    })


# 封装到类中，直接调用
def user(request):
    pager = Pagination(request.GET.get('page', '1'), len(all_user), per_num=10, max_show=15)

    return render(request, 'consultant/user.html', {
        "all_user": all_user[pager.start:pager.end],
        'page_html': pager.page_html
    }, )


def customer_add(request):
    form_obj = forms.CustomerForm()
    if request.method == 'POST':
        form_obj = forms.CustomerForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('customer_list'))
    return render(request, 'consultant/customer_add.html', {'form_obj': form_obj})


def customer_edit(request, edit_id):
    obj = models.Customer.objects.filter(pk=edit_id).first()
    form_obj = forms.CustomerForm(instance=obj)
    if request.method == 'POST':
        form_obj = forms.CustomerForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('customer_list'))
    return render(request, 'consultant/customer_edit.html', {'form_obj': form_obj})


def customer_change(request, edit_id=None):
    obj = models.Customer.objects.filter(pk=edit_id).first()
    form_obj = forms.CustomerForm(instance=obj)  # 包含数据
    if request.method == 'POST':
        form_obj = forms.CustomerForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()  # 有instance是修改数据，无则增加数据
            return redirect(revers_url(request, 'customer_list'))
    return render(request, 'consultant/customer_change.html', {'form_obj': form_obj, 'edit_id': edit_id})


def consult_list(request, customer_id):
    if customer_id == '0':
        all_consult = models.ConsultRecord.objects.filter(consultant=request.account)
    else:
        all_consult = models.ConsultRecord.objects.filter(consultant=request.account, customer_id=customer_id)
    return render(request, 'consultant/consult_list.html', {'all_consult': all_consult})


def consult_add(request):
    obj = models.ConsultRecord(consultant=request.account)
    form_obj = forms.ConsultForm(instance=obj)
    if request.method == 'POST':
        form_obj = forms.ConsultForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('consult_list', kwargs={'customer_id': '0'}))
    return render(request, 'consultant/consult_add.html', {'form_obj': form_obj})


def consult_edit(request, edit_id):
    obj = models.ConsultRecord.objects.filter(pk=edit_id).first()
    form_obj = forms.ConsultForm(instance=obj)
    if request.method == 'POST':
        form_obj = forms.ConsultForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('consult_list', kwargs={'customer_id': '0'}))
    return render(request, 'consultant/consult_edit.html', {'form_obj': form_obj})


class EnrollmentList(View):
    def get(self, request, customer_id='0'):
        if customer_id == '0':
            all_enrollment = models.Enrollment.objects.all()
        else:
            all_enrollment = models.Enrollment.objects.filter(customer_id=customer_id)

        return render(request, 'consultant/enrollment_list.html', {'all_enrollment': all_enrollment})


def enrollment_add(request, customer_id):
    obj = models.Enrollment(customer_id=customer_id)
    form_obj = forms.EnrollmentForm(instance=obj)
    if request.method == 'POST':
        form_obj = forms.EnrollmentForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('enrollment_list', kwargs={'customer_id': '0'}))

    return render(request, 'consultant/enrollment_add.html', {'form_obj': form_obj})


def enrollment_edit(request, enrollment_id):
    obj = models.Enrollment.objects.filter(pk=enrollment_id).first()
    form_obj = forms.EnrollmentForm(instance=obj)
    if request.method == 'POST':
        form_obj = forms.EnrollmentForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('enrollment_list', kwargs={'customer_id': '0'}))
    return render(request, 'consultant/enrollment_edit.html', {'form_obj': form_obj})


def enrollment_change(request, enrollment_id=None, customer_id=None):
    obj = models.Enrollment.objects.filter(pk=enrollment_id).first() if enrollment_id else models.Enrollment(
        customer_id=customer_id)
    form_obj = forms.EnrollmentForm(instance=obj)
    if request.method == 'POST':
        form_obj = forms.EnrollmentForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('enrollment_list', kwargs={'customer_id': '0'}))
    # return render(request, 'enrollment_edit.html' if enrollment_id else 'enrollment_add.html', {'form_obj': form_obj})
    return render(request, 'consultant/enrollment_edit.html' if enrollment_id else 'consultant/enrollment_add.html', {'form_obj': form_obj})
