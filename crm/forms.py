#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from crm import models
from django.core.exceptions import ValidationError
import hashlib


class BootstrapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)         # 不兼容py2.7
        super(BootstrapForm, self).__init__(*args, **kwargs)
        for i in self.fields.values():
            i.widget.attrs.update({'class': 'form-control'})


class RegisterForm(BootstrapForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='密码', min_length=6, required=False,
                               error_messages={'required': '不能为空', 'invalid': '格式错误'})
    re_password = forms.CharField(widget=forms.PasswordInput(), label='确认密码', min_length=6,
                                  error_messages={'required': '不能为空', 'invalid': '格式错误'})

    class Meta:
        model = models.UserProfile
        # fields = '__all__'  # 所有字段
        # fields = ['username', 'password']
        exclude = ['is_active']
        labels = {
            'username': '用户名',
            'password': '密码',
            're_password': '确认密码',
            'department': '部门',
            'memo': '备注',
            'mobile': '手机号',
        }

        error_messages = {
            'username': {
                'required': '不能为空',
                'invalid': '账号格式错误',
            },
            'name': {
                'required': '不能为空',
                'invalid': '名称格式错误',
            },

        }

    def clean(self):
        pwd = self.cleaned_data.get('password', '')
        re_pwd = self.cleaned_data.get('re_password')
        if pwd and re_pwd == pwd:
            md5 = hashlib.md5()
            md5.update(pwd.encode('utf-8'))
            en_pwd = md5.hexdigest()
            self.cleaned_data['password'] = en_pwd
            return self.cleaned_data
        self.add_error('re_password', '两次密码不一致')
        raise ValidationError('两次密码不一致')


class CustomerForm(BootstrapForm):
    class Meta:
        model = models.Customer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields.get('course').widget.attrs.update({'class': ''})


class ConsultForm(BootstrapForm):
    class Meta:
        model = models.ConsultRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.get('delete_status').widget.attrs.pop('class')

        customer_choices = [(i.pk, str(i)) for i in self.instance.consultant.customers.all()]
        customer_choices.insert(0, ('', '---------'))

        self.fields['customer'].choices = customer_choices
        # print(list(self.fields['customer'].widget.choices))
        self.fields['consultant'].choices = [(self.instance.consultant.pk, self.instance.consultant.name)]


class EnrollmentForm(BootstrapForm):
    class Meta:
        model = models.Enrollment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.customer_id != '0':
            # 限制客户是当前的客户
            self.fields['customer'].choices = [(self.instance.customer_id, str(self.instance.customer))]
            # 限制客户可选的班级是记录中已报的班级
            self.fields['enrolment_class'].choices = [(i.pk, str(i)) for i in self.instance.customer.class_list.all()]
            # 限制客户可选的校区是记录中已报的校区
            self.fields['enrolment_class'].choices = [(i.pk, str(i)) for i in self.instance.customer.class_list.all()]


class ClassForm(BootstrapForm):
    class Meta:
        model = models.ClassList
        fields = '__all__'


class CourseRecordForm(BootstrapForm):
    class Meta:
        model = models.CourseRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 限制讲师是当前的讲师
        self.fields['teacher'].choices = [(self.instance.teacher_id, str(self.instance.teacher))]
        # 限制班级是当前班级
        self.fields['re_class'].choices = [(self.instance.re_class_id, str(self.instance.re_class))]


class StudyRecordForm(BootstrapForm):
    class Meta:
        model = models.StudyRecord
        fields = '__all__'
