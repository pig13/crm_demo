from django.conf import settings


# 动态设置一级菜单
def init_permission(request, obj):
    """
    权限信息初始化，将权限信息保存到session中
    :param request:
    :param obj:
    :return:
    """
    ret = obj.role.all().filter(permission__url__isnull=False) \
        .values('permission__url', 'permission__title', 'permission__is_menu', 'permission__icon').distinct()

    permission_list = []
    menu_list = []
    for i in ret:
        permission_list.append({'url': i['permission__url']})
        if i['permission__is_menu']:
            menu_list.append(
                {'title': i['permission__title'], 'icon': i.get('permission__icon'), 'url': i['permission__url']})
    # 权限信息
    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    # 菜单信息
    request.session[settings.MENU_SESSION_KEY] = menu_list


# 动态设置二级菜单
def init_permission(request, obj):
    """
    权限信息的初识化
    保存权限和菜单的信息
    :param request:
    :param obj:
    :return:
    """
    ret = obj.role.all().filter(permission__url__isnull=False).values('permission__url',
                                                                      'permission__title',
                                                                      'permission__menu__title',
                                                                      'permission__menu__icon',
                                                                      'permission__menu__weight',
                                                                      'permission__menu_id',
                                                                      'permission__id',
                                                                      'permission__name',
                                                                      'permission__parent__name',
                                                                      'permission__parent__id',
                                                                      ).distinct()

    # 存放权限信息
    permission_dict = {}
    # 存放菜单信息
    menu_dict = {}
    for item in ret:
        # 将所有的权限信息添加到permission_dict
        permission_dict[item['permission__name']] = {
            'url': item['permission__url'],
            'id': item['permission__id'],
            'pname': item['permission__parent__name'],
            'pid': item['permission__parent__id'],
            'title': item['permission__title']
        }

        # 构造菜单的数据结构
        menu_id = item.get('permission__menu_id')

        # 表示当前的权限是不做菜单的权限
        if not menu_id:
            continue

        # 可以做菜单的权限
        if menu_id not in menu_dict:
            menu_dict[menu_id] = {
                'title': item['permission__menu__title'],  # 一级菜单标题
                'icon': item['permission__menu__icon'],
                'weight': item['permission__menu__weight'],
                'children': [{
                    'title': item['permission__title'],
                    'url': item['permission__url'],
                    'id': item['permission__id'],
                }]
            }
        else:
            menu_dict[menu_id]['children'].append({
                'title': item['permission__title'],
                'url': item['permission__url'],
                'id': item['permission__id'],
            })

    # 保存权限信息
    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict

    # 保存菜单信息
    request.session[settings.MENU_SESSION_KEY] = menu_dict
