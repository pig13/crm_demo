from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views import View
from django.forms import modelformset_factory

from crm import forms
from crm import models
from crm.utils.pagination import Pagination
from crm.utils.url import revers_url, rev_url


class ClassList(View):
    def get(self, request):
        q = self.search([])
        all_class = models.ClassList.objects.filter(q)

        pager = Pagination(request.GET.get('page', '1'), len(all_class), params=request.GET.copy(), per_num=10,
                           max_show=15)

        return render(request, 'teacher/class_list.html', {
            'all_class': all_class[pager.start:pager.end],
            'page_html': pager.page_html,
        })

    def post(self, request):
        res = None
        if hasattr(self, request.POST.get('action')):
            res = getattr(self, request.POST.get('action'))()
        # 如果没有抢到
        if res:
            return res
        return redirect(reverse('class_list'))

    def search(self, query_list):
        query = self.request.GET.get('query', '')
        q = Q()
        q.connector = 'OR'
        # Q(qq__contains=query)   <==>   Q(('qq__contains',query))
        for i in query_list:
            q.children.append(Q(('{}__contains'.format(i), query)))
        return q


def class_change(request, class_id=None):
    obj = models.ClassList.objects.filter(pk=class_id).first()
    form_obj = forms.ClassForm(instance=obj)
    title = '编辑班级' if class_id else '新增班级'
    if request.method == 'POST':
        form_obj = forms.ClassForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(rev_url(request, 'class_list'))
    return render(request, 'form.html', {'form_obj': form_obj, 'title': title})


class CourseRecordList(View):
    def get(self, request, class_id):
        q = self.search([])
        all_course_record = models.CourseRecord.objects.filter(q, re_class_id=class_id)

        pager = Pagination(request.GET.get('page', '1'), len(all_course_record), params=request.GET.copy(), per_num=10,
                           max_show=15)

        return render(request, 'teacher/course_record_list.html', {
            'all_course_record': all_course_record[pager.start:pager.end],
            'page_html': pager.page_html,
            'class_id': class_id,
        })

    def post(self, request, class_id=None):
        res = None
        if hasattr(self, request.POST.get('action')):
            res = getattr(self, request.POST.get('action'))()
        # 如果没有抢到
        if res:
            return res
        return redirect(reverse('course_record_list', kwargs={'class_id': class_id}))

    def search(self, query_list):
        query = self.request.GET.get('query', '')
        q = Q()
        q.connector = 'OR'
        # Q(qq__contains=query)   <==>   Q(('qq__contains',query))
        for i in query_list:
            q.children.append(Q(('{}__contains'.format(i), query)))
        return q

    def study_record_init(self):
        course_record_ids = self.request.POST.get('pk')
        course_record_obj_list = models.CourseRecord.objects.filter(pk__in=course_record_ids)
        for course_record_obj in course_record_obj_list:
            all_students = course_record_obj.re_class.customer_set.all().filter(status='studying')
            study_record_list = []
            for student in all_students:
                study_record_list.append(models.StudyRecord(course_record=course_record_obj, student=student))
            models.StudyRecord.objects.bulk_create(study_record_list)  # 批量创建数据


def course_record_change(request, class_id=None, course_record_id=None):
    obj = models.CourseRecord(re_class_id=class_id, teacher=request.account) if \
        class_id else models.CourseRecord.objects.filter(pk=course_record_id).first()
    form_obj = forms.CourseRecordForm(instance=obj)
    title = '新增课程记录' if class_id else '编辑课程记录'
    if request.method == 'POST':
        form_obj = forms.CourseRecordForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(rev_url(request, 'course_record_list', class_id if class_id else obj.re_class_id))
    return render(request, 'form.html', {
        'form_obj': form_obj,
        'title': title,
    })


def study_record(request, course_record_id):
    FormSet = modelformset_factory(models.StudyRecord, forms.StudyRecordForm, extra=0)

    all_study_record = models.StudyRecord.objects.filter(course_record_id=course_record_id)

    form_obj = FormSet(queryset=all_study_record)

    if request.method == 'POST':
        form_obj = FormSet(request.POST, queryset=all_study_record)
        if form_obj.is_valid():
            form_obj.save()

    return render(request, 'teacher/study_record_list.html', {
        'form_obj': form_obj
    })
