from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import HttpResponse, redirect, reverse
import re


class RbacMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 1. 获取当前url
        url = request.path_info
        # 2. 检测白名单
        for i in settings.WHITE_LIST:
            if re.match(i, url):
                return
        # 3.获取当前用户权限信息
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)

        if not permission_dict:
            return redirect(reverse('login'))

        # 登录但不需要权限校验
        for i in settings.NO_PEREMISSION_LIST:
            if re.match(i, url):
                return
        # request.breadcrumb_list = [
        #     {'url': 'index', 'title': '首页'},
        # ]
        setattr(request, settings.BREADCRUMB, [{'url': '/index/', 'title': '首页'}])

        # 4. 权限的校验
        for i in permission_dict.values():
            if re.match(r'^{}$'.format(i['url']), url):
                pid = i.get('pid')
                id = i.get('id')
                pname = i.get('pname')
                if pid:
                    # 有PID表示当前访问的权限是子权限，他有父权限，要让这个父权限展开
                    setattr(request, settings.CURRENT_MENU, pid)
                    # request.permission_id = pid
                    p_dict = permission_dict[pname]
                    getattr(request, settings.BREADCRUMB).append({'url': p_dict['url'], 'title': p_dict['title']})
                    getattr(request, settings.BREADCRUMB).append({'url': i['url'], 'title': i['title']})
                    # request.breadcrumb_list.append({'url': p_dict['url'], 'title': p_dict['title']})
                    # request.breadcrumb_list.append({'url': i['url'], 'title': i['title']})
                else:
                    # 无PID表示当前访问的权限是父权限，要让自己展开
                    setattr(request, settings.CURRENT_MENU, id)
                    # request.permission_id = id

                    # 导航信息
                    getattr(request, settings.BREADCRUMB).append({'url': i['url'], 'title': i['title']})
                    # request.breadcrumb_list.append({'url': i['url'], 'title': i['title']})

                return
        # 拒绝访问
        return HttpResponse('没有权限！')
