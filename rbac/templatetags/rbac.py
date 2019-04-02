from django import template
from django.conf import settings
import re
from collections import OrderedDict

register = template.Library()


# 一级动态菜单
# @register.inclusion_tag('rbac/menu.html')
# def menu(request):
#     menu_list = request.session.get(settings.MENU_SESSION_KEY)
#     for i in menu_list:
#         if re.match('^{}$'.format(i['url']), request.path_info):
#             i['class'] = 'active'
#             break
#     return {'menu_list': menu_list}

# 二级动态菜单
@register.inclusion_tag('rbac/menu.html')
def menu(request):
    menu_dict = request.session.get(settings.MENU_SESSION_KEY)
    url = request.path_info

    order_dict = OrderedDict()

    # for i in sorted(menu_dict, key=lambda x: menu_dict[x]['weight'], reverse=True):
    #     order_dict[i] = menu_dict[i]
    #
    # for value in order_dict.values():
    #     for i in value['children']:
    #         if re.match('^{}$'.format(i['url']), url):
    #             i['class'] = 'active'
    #             break

    for i in sorted(menu_dict, key=lambda x: menu_dict[x]['weight'], reverse=True):
        item = order_dict[i] = menu_dict[i]  # 赋值到有序菜单，并取出一级菜单信息
        item['class'] = 'hide'
        for j in item['children']:
            # if re.match('^{}$'.format(j['url']), url):
            if j['id'] == getattr(request, settings.CURRENT_MENU):
                j['class'] = 'active'
                item['class'] = ''
                break
    return {'menu_list': order_dict.values()}


@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    breadcrumb_list = getattr(request, settings.BREADCRUMB)
    return {'breadcrumb_list': breadcrumb_list}


@register.filter()
def has_permission(request, name):
    if name in request.session.get(settings.PERMISSION_SESSION_KEY):
        return True


@register.filter()
def type_obj(obj):
    return type(obj)


@register.simple_tag
def gen_role_url(request, rid):
    params = request.GET.copy()
    params['rid'] = rid
    return params.urlencode()
