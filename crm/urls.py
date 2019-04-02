from django.conf.urls import url
from crm.views import consultant
from crm.views import teacher

urlpatterns = [
    # 销售

    # 公户
    # url(r'^customer_list/', consultant.customer_list, name='customer_list'),
    url(r'^customer_list/', consultant.CustomerList.as_view(), name='customer_list'),
    # 私户
    # url(r'^customer_my/', consultant.customer_list, name='customer_my'),
    url(r'^customer_my/', consultant.CustomerList.as_view(), name='customer_my'),
    url(r'^customer_add/', consultant.customer_change, name='customer_add'),
    url(r'^customer_edit/(\d+)/', consultant.customer_change, name='customer_edit'),
    # url(r'^customer_change/(\d+)/', consultant.customer_change, name='customer_change'),

    # 跟进记录
    url(r'^consult_list/(0)', consultant.consult_list, name='consult_list_all'),
    url(r'^consult_list/(?P<customer_id>\d+)', consultant.consult_list, name='consult_list'),
    url(r'^consult_add/', consultant.consult_add, name='consult_add'),
    url(r'^consult_edit/(\d+)', consultant.consult_edit, name='consult_edit'),

    # 报名记录
    url(r'^enrollment_list/(0)', consultant.EnrollmentList.as_view(), name='enrollment_list_all'),
    url(r'^enrollment_list/(?P<customer_id>\d+)', consultant.EnrollmentList.as_view(), name='enrollment_list'),
    url(r'^enrollment_add/(?P<customer_id>\d+)', consultant.enrollment_change, name='enrollment_add'),
    url(r'^enrollment_edit/(?P<enrollment_id>\d+)', consultant.enrollment_change, name='enrollment_edit'),

    # url(r'^user/', consultant.user),      # 测试分页使用

    # 教师
    # 班级展示
    url(r'^class_list/', teacher.ClassList.as_view(), name='class_list'),
    url(r'^class_add/', teacher.class_change, name='class_add'),
    url(r'^class_edit/(?P<class_id>\d+)/', teacher.class_change, name='class_edit'),

    # 课程记录
    url(r'^course_record_list/(?P<class_id>\d+)', teacher.CourseRecordList.as_view(), name='course_record_list'),
    url(r'^course_record_add/(?P<class_id>\d+)', teacher.course_record_change, name='course_record_add'),
    url(r'^course_record_edit/(?P<course_record_id>\d+)/', teacher.course_record_change, name='course_record_edit'),

    # 学习记录
    url(r'^study_record/(?P<course_record_id>\d+)', teacher.study_record, name='study_record'),

]
