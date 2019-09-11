
# CRM项目
CRM(customer relationship management)   客户关系管理系统
## 项目简介
本系统使用者有销售、老师、管理员，主要用来管理客户，维护和客户的关系，基于RBAC对使用系统人员进行权限控制，对老师、班级和销售进行统一管理。
## 功能特性
1. 登录
2. 注册
3. 销售：
    1. 客户管理
        1. 增加、编辑客户信息
    2. 跟进的管理
        1. 增加、编辑跟进的信息
    3. 报名记录
        1. 增加和编辑报名记录
4. 讲师：
    1. 班级管理
        1. 增加、编辑班级信息
    2. 课程管理
        1. 增加、编辑课程信息
    3. 上课记录的管理
        1. 增加、编辑课程信息
5. 权限管理
    1. 角色管理
        1. 增加、删除、修改角色
    2. 菜单管理
        1. 增加、删除、修改菜单
    3. 分配权限
        1. 增加、删除、修改用户、角色的权限信息



## 表结构设计

权限相关

1. 用户表
2. 权限表
3. 角色表
4. 菜单表

应用相关

1. 客户表
    客户个人信息，qq,姓名，电话，状态（缴费，未交费）
2. 用户表  
    1. 销售  助教 ID 账号 密码 姓名 部门
3. 部门表 
4. 班级表
5. 跟进记录表
6. 报名记录表
7. 缴费记录表
8. 课程记录表
9. 上课记录表



## 部署
0. 安装依赖，`pip install -r requirements.txt`
1. 运行项目，`python manage.py runserver  0.0.0.0:80`
5. 登录django-admin填充数据
3. 测试运行
   1. admin账号  admin,admin123
   2. 测试账号， test， test 
   3. 销售账号，teacher，teacher
   4. 讲师账号， seller，seller



## 目录结构描述
```text

----------------------------------------------------------
crm_demo:
   |--Alibaba_crm           项目目录             
   |  |--init.py     
   |  |--settings.py        项目配置文件     
   |  |--urls.py            URL根配置     
   |  |--wsgi.py            内置runserver命令的WSGI应用配置     
   |     
   |--crm                   业务逻辑目录                 
   |  |--middleware         中间件
   |  |  |--*
   |  |--migrations         数据库迁移，版本控制         
   |  |  |--*
   |  |--templates          模板文件
   |  |  |--*
   |  |--templatetags       模板中的标签和自定义filter
   |  |  |--*   
   |  |--utils              工具包
   |  |  |--*
   |  |--views              视图
   |  |  |--*
   |  |--admin.py           后台         
   |  |--apps.py            app设置
   |  |--forms.py           表单，用户提交的数据，对数据验证及在模板中输入框的生成
   |  |--models.py          数据库相关，存取数据时用到
   |  |--urls.py            app的url配置
   |  |--test.py            
   |  |--__init__.py
   | 
   |--rbac                  权限控制目录                 
   |  |--middleware         中间件
   |  |  |--*
   |  |--migrations         数据库迁移，版本控制         
   |  |  |--*
   |  |--service            服务器权限信息
   |  |  |--__init__.py     
   |  |  |--permission.py   初始化权限
   |  |  |--routes.py       获取所有url
   |  |--static             静态资源
   |  |  |--*
   |  |--templates          模板文件
   |  |  |--*
   |  |--templatetags       模板中的标签和自定义filter
   |  |  |--*   
   |  |--views              视图
   |  |--admin.py           后台         
   |  |--apps.py            app设置
   |  |--forms.py           表单，用户提交的数据，对数据验证及在模板中输入框的生成
   |  |--models.py          数据库相关，存取数据时用到
   |  |--urls.py            app的url配置
   |  |--icon_spider.py     爬取icon
   |  |--test.py            
   |  |--__init__.py
   | 
   |--static                静态资源目录    
   |  |--* 
   |
   |--templates             模板文件目录                 
   |  |--login.html
   |  |--register.html
   |
   |--manager.py            管理文件
   |
   |--README.md                 

   
----------------------------------------------------------

```



===================以下是开发时所作的笔记================================

## 权限相关

### 权限设计

1.为什么要有权限？

2.开发一个权限的组件，为什么要开发组件？

3.什么是权限？

在web开发中 url代表权限

4.权限表结构设计

权限表    角色表   用户表

权限和角色的多对多关系表       用户和角色的多对多关系表

RBAC  基于角色的权限控制

```python
from django.db import models


class Permission(models.Model):
    """
    权限表
    """
    url = models.CharField(max_length=32, verbose_name='权限')
    title = models.CharField(max_length=32, verbose_name='标题')

    def __str__(self):
        return self.title


class Role(models.Model):
    """
    角色表
    """
    name = models.CharField(max_length=32, verbose_name='名称')
    permission = models.ManyToManyField(to='Permission', verbose_name='角色拥有的权限')

    def __str__(self):
        return self.name


class User(models.Model):
    """
    用户表
    """
    name = models.CharField(max_length=32, verbose_name='名称')
    password = models.CharField(max_length=32, verbose_name='密码')
    role = models.ManyToManyField(to='Role', verbose_name='用户拥有的角色')

    def __str__(self):
        return self.name

```


在Django admin 中增删改查数据
1. 可以再注册网站中加上 ModelAdmin，可以直接修改数据，不用再点进去
```python
from django.contrib import admin
from rbac import models


# Register your models here.
class PermissionModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'url']  # 展示的字段
    list_editable = ['url']  # 编辑的字段


admin.site.register(models.Role)
admin.site.register(models.Permission, PermissionModelAdmin)
admin.site.register(models.User)

```

5.流程
    1. 如果登录验证成功，在views中设置session.
        1. session中保存的是json数据
        2. session权限Key放在settings文件中， 可配置
        3. session中放置 url 和 title
        2. 中间件权限校验
        1. 获取当前URL，如果在白名单中允许访问
            1. 白名单在settings文件中配置
        2. 获取当前用户的权限信息
        3. 权限的校验
            1. 校验使用正则match匹配
            2. 权限信息应为正则表达式
            3. 如果匹配则允许访问
            4. 如果全部匹配不成功，则拒绝访问

```python
class RbacMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 1. 获取当前url
        url = request.path_info
        # 2. 检测白名单
        for i in settings.WHITE_LIST:
            if re.match(i, url):
                return
        # 3.获取当前用户权限信息
        permission_list = request.session.get(settings.PERMISSION_SESSION_KEY)

        # 4. 权限的校验
        for i in permission_list:
            if re.match(r'^{}$'.format(i['permission__url']), url):
                return
        # 拒绝访问
        return HttpResponse('没有权限！')

```

   

### 动态生成一级菜单
将菜单信息写到session中，在template中使用 inclusion_tag 解析数据生成 HTML组件



### 动态生成二级菜单

信息列表  -  一级菜单

	客户列表  - 二级菜单

财务列表

	缴费列表

新建Menu表，收录一级菜单信息
```python
class Menu(models.Model):
    """
    菜单表     一级菜单
    """
    title = models.CharField(max_length=32)
    icon = models.CharField(max_length=32, null=True, blank=True, verbose_name='图标')

    def __str__(self):
        return self.title


class Permission(models.Model):
    """
    权限表
    可以做二级菜单的权限   menu 关联 菜单表
    不可以做菜单的权限    menu=null
    """
    url = models.CharField(max_length=32, verbose_name='权限')
    title = models.CharField(max_length=32, verbose_name='标题')
    menu = models.ForeignKey(to='Menu', null=True, blank=True)

    def __str__(self):
        return self.title

```


设计存储菜单信息的数据结构
```python
data = [{
	'permissions__url': '/customer/list/',
	'permissions__title': '客户列表',
	'permissions__menu__title': '信息列表',
	'permissions__menu__icon': 'fa-code-fork',
	'permissions__menu_id': 1
},
    {
	'permissions__url': '/customer/list/',
	'permissions__title': '用户列表',
	'permissions__menu__title': '信息列表',
	'permissions__menu__icon': 'fa-code-fork',
	'permissions__menu_id': 1
},{
	'permissions__url': '/customer/add/',
	'permissions__title': '增加客户',
	'permissions__menu__title': None,
	'permissions__menu__icon': None,
	'permissions__menu_id': None
}, {
	'permissions__url': '/customer/edit/(\\d+)/',
	'permissions__title': '编辑客户',
	'permissions__menu__title': None,
	'permissions__menu__icon': None,
	'permissions__menu_id': None
}]


"""
{
  
  1:{
  	'title':'信息列表',
  	'icnon':'fa-code-fork',
    'children': [
    	{'title': '客户列表','url':'/customer/list/ },
    	{'title': '用户列表','url':'/customer/list/ }
    ]
  	
  }

}

"""
```


#### 二级菜单优化

一级菜单的排序：

1. 加一个weight的字段  ，权重越大越靠前
2. 有序字典

```
from collections import OrderedDict
```

3. 
```
   # sorted  按照权重的大小对字典的key进行排序
   for i in sorted(menu_dict, key=lambda x: menu_dict[x]['weight'], reverse=True):
       order_dict[i] = menu_dict[i]
```






### 非菜单权限的归属问题
菜单目录   
```text
信息列表
	客户列表
		添加客户     （这个菜单不会展示，但属于客户列表的操作）
		编辑客户
财务列表
	缴费列表
```
需求：用户发起 编辑客户/添加客户 请求时，客户列表会显示    
解决方案:在权限表中增加外键parent_id自关联，在动态渲染菜单时，改为id匹配（菜单session中的权限id 与 请求的权限的parent_id）。  

1. 修改表结构，在权限表中增加 parent_id 外键，自关联。
2. 修改登录初始权限信息，从数据库中取出权限表的 id 和 parent__id(pid)，将id、pid存入权限session中，将id存入菜单session中
3. 修改中间件，在权限验证成功后获取当前权限的pid,id,若有pid则把pid存入request.permission_id中，否则把id存入request.permission_id中 
4. 修改template中菜单inclusion_tag中的验证方式，把原先的url匹配换成 request.permission_id 与 菜单session中的id 匹配


```text
权限表
id   url       title                menu_id  parent_id
1      /list/    客户列表             1              null 
2     /add/   添加客户              null             1

```


### 路径导航

权限信息放入到session中。进行json序列化字段的key 如果是数字key，会变成数字字符串

在request定义的值都写到settings中，采用反射动态赋值，取值

### 权限控制到按钮级别
1. 权限表增加字段，name， URL的别名
2. 修改权限session的数据机构，key改为 name，URL的别名，从数据库中获取name,panme相应信息， 相应使用原来的key id 的地方加以修改
3. 自定义filter(request,name),判断name 是否在用户的权限信息中，返回布尔值
4. 在template中应用自定义filter，判断URL别名是否在权限信息中

### 内容总结

1. 中间件
   本质是一个类，在请求经过WSGI后第一个经过中间件。中间件里面有五个方法，分别对应不同情况的调用。

2. form modelform modelformset 

3. cookie和session
4. ORM操作
5. 自定义的filter simple_tag   inclusion_tag
6. Django
7. 权限

#### 权限控制

- 什么是权限？

  一个URL对应一个权限 

#### 表结构  4个model  6张表

菜单表

- title 标题
- icon 图标
- weight 权重 

权限表

 - url

 - title  标题

 - name   URL别名,权限控制到按钮级别用

 - menu 外键  关联菜单表，如果有有它，则表示自己是二级菜单

 - parent 外键  关联自己，如果有有它，表示自己是三级菜单，点击它让父级菜单展示

角色表

- title 标题

- permissions 多对多  关联权限

用户表

- name 用户名

- pwd   密码

- roles  多对多  关联角色

角色和权限的关系表

用户和角色的关系表

#### 验证流程

##### 中间件

- 白名单

	- settings

	- 正则匹配 

- 获取权限

- 需要登录不需要校验的URL的校验

- 路径导航 request.breadcrumb_list=[ { 首页   url  }  ]

- 权限的校验

	- 正则

	- 判断pid  

		- 没有pid   表示当前访问的权限是二级菜单

			记录request.current_menu_id = id  

			路径导航

				request.breadcrumb_list.append({  url  title  })

		- 有pid    表示当前访问的权限是二级菜单下的一个子权限

			记录request.current_menu_id = pid 

			路径导航

				获取父权限的信息    permission_dict[str(pid)]      permission_dict[  pname ]
			
				request.breadcrumb_list.append({  url  title  })   # 父权限  二级菜单
			
				request.breadcrumb_list.append({  url  title  })

	- 匹配成功return

- return HTTPResponse('没权限')

##### 登录成功进行权限信息的初始化

- 获取当前用户的所有权限

	- ORM

	- 去除权限为空的

	- 跨表  去重

- 构建数据结构

	- 权限的字典

	  ```
  permission_dict = {
	  	'URL的别名' ：{ ‘url’    ， ‘title’ ，   ’id‘  , 'pid'  'pname'   }
  }
	    id和pid主要用于二级菜单的展示，和访问三级菜单时二级菜单展示（三级菜单，非菜单权限信息，不会展示，但归属与二级菜单）
      name，用于权限控制到按钮级别
      pname,原来是用id作为字典的key，换成name后，需要用pname获取父级权限信息
    ```

	- 菜单的字典

	  ```
  menu_dict ={
	      '一级菜单的ID'：{ 
	              ’title‘ 
	               ’icon‘ 
	              ’weight‘  
	              ’children‘:[ 
	                      {'二级菜单的title'   ’url‘   'id'  }
	                   ]
	        }
	  
	  	}
	  ```
	
- 放入到session中

	- settings配置

	- json序列化   数字当做字典的KEY 会变成字符串

- 模板

  - 母版和继承

  - 自定义inclusion_tag

  	- 动态生成二级菜单

  		- settings

  		- sorted

  		- 有序字典

  	- 路径导航

  		- settings

  		- 反射

  - 自定义filter

  	- 权限控制到按钮级别  
  	
  	  ```
  	  namespace:name
  	  {%   if  request|has_permission:'namespace:name ' %}
  	  {% endif %}
  	  ```

  - URL 反向解析



### 开发中出现的问题
1. views传给template中的数据，在模板中需要比较判断时，常因数据类型不用而显示不出效果
    1. views中 把数据json后，如果数字作为key，json后key会变成str类型
        - 权限信息放入到session中。进行json序列化字段的key 如果是数字key，会变成数字字符串

    

### 应用权限组件

1. 拷贝rbac组件到新的项目中，注册app
2. 修改用户表，继承rbac中的User

```
class User(models.Model):
    """
    用户表
    """
    # name = models.CharField(max_length=32, verbose_name='名称')
    # password = models.CharField(max_length=32, verbose_name='密码')
    roles = models.ManyToManyField(Role, verbose_name='用户拥有的角色', blank=True)

    # def __str__(self):
    #     return self.name
    class Meta:
        abstract = True  # 数据库迁移时候不会生成表，用来做基类

class UserProfile(User, models.Model):
    pass
```

3. 执行数据库迁移的命令
   1. 删除rbac下migrations中的记录
   2. 注释掉admin中User表
   3. roles = models.ManyToManyField(Role, verbose_name='用户拥有的角色', blank=True) # 关联的字段不要写成字符串形式
   4. 迁移，`python manager.py makemigrations` , `python manager.py migrate`
4. 设置rbac的url

```python
url(r'rbac/', include('rbac.urls',namespace='rbac'))
```

5. 菜单管理  
   访问接口，`/rbac/menu/list/` 添加一级菜单

6. 权限的录入
   1. 所有的url要有name
   2. 不要忽略rbac namespace
   3. 通过批量操作录入权限
     1. 构建层级结构
     2. 注意url和别名的长度(是否超过数据库限制)
     3. 属于菜单的URL将直接添加到模板中，不能含有动态参数(或者设置固定参数),不能含有`^$`等元字符

7. 角色管理
   1. 访问接口 `/rbac/role/list/` ,增加角色

8. 分配权限
   1. 访问 `/rbac/distribute/permission/` 分配权限
   2. 注意用新的用户表替换rbac中的User
   3. 给不同角色分配权限
   4. 给不同用户分配角色

9. 应用上权限

   1. 应用中间件   在settings中写上权限的配置



    MIDDLEWARE = [
        ...
        'rbac.middleware.rbac.RbacMiddleware',
        ...
    ]
    # 权限kEY
    PERMISSION_SESSION_KEY = 'permission'
    # 菜单KEY
    MENU_SESSION_KEY = 'menu'
    
    WHITE_LIST = [
        r'^/login/$',
        r'^/register/$',
        r'^/admin/.*',
    ]
    NO_PEREMISSION_LIST = [
        r'^/index/$',
        r'^/logout/$',
    ]
    
    # 路径导航
    BREADCRUMB = 'breadcrumb_list'
    # 当前菜单ID
    CURRENT_MENU = 'current_parent_id'


   2. 登录成功后权限信息的初识化
   ```
from rbac.service.permission import init_permisson
# 权限信息的初始化
init_permisson(request,obj)
   ```

10. 动态生成二级菜单

    1. 在layout中使用

~~~html
```
导入CSS js 
{% load rbac %}
{% menu request %}
```
~~~

11. 应用路径导航

    ```HTML
    {% breadcrumb request %}
    ```

12. 权限控制到按钮级别

```python
{% load rbac %}
{% if request|has_permission:"consult_add" %}
    <a href="{% url 'consult_add' %}" class="btn btn-primary btn-sm">添加</a>
{% endif %}
```







## 应用相关

[](隐藏链接)
[](http://www.cnblogs.com/huchong/articles/8185125.html)
[](https://www.cnblogs.com/wupeiqi/articles/10143677.html)


### 展示客户

1. 模板的查找顺序：

​	先找全局的templates——》 按照app的注册顺序找templates中的文件

2. 使用admin添加数据：
    1. 创建超级用户

       python manage.py  createsuperuser

   2. 在admin中注册model

   ```python
   from django.contrib import admin
   from crm import models
   
   admin.site.register(models.Customer)
   admin.site.register(models.ClassList)
   admin.site.register(models.Campuses)
   ```

   3. 使用http://127.0.0.1:8000/admin 添加数据

3. 不同字段的显示

   1. 普通字段 
      
    ```
        {{ customer.qq }}
    ```

   ​     {{ customer.get_sex_display }}    # get_字段名_display() 方法  模板中不加（）

   3. 时间日期字段
    ```
        1. 单个设置
        <td>{{ customer.date|date: 'Y-m-d H:m:s' }}</td>
        2. 全部修改，在settings设置
        USE_L10N = False
        DATETIME_FORMAT = "Y-m-d H:m:s"
        DATE_FORMAT = "Y-m-d"
    ```
   
   4. 其他字段
   
      多对多、特殊显示，在model中定义方法。

      ```python
   def show_classes(self):
          return ' | '.join([str(i) for i in self.class_list.all()])
   
      def show_status(self):
          color_dict = {
              'signed': 'green',
              'unregistered': 'red',
              'studying': 'blue',
              'paid_in_full': 'yellow',
          }
      
          return '<span style="background-color: {};color: white;padding: 3px">{}</span>'.format(
              color_dict.get(self.status),
              self.get_status_display())
      ```

### 分页


### 增加客户
1. 增加路由
2. 增加视图函数
3. 增加模板文件
    1. 使用bootstrap面板 ，好看
    2. 循环form_obj，每个都是field，在`django BaseForm __iter__`函数中有体现
    3. bootstrap表单，校验状态，校验失败会有颜色变化
4. 增加ModelForm,在视图中调用

### 编辑客户
ModelForm() 中加 instance 实例，里面将直接填充数据
```python
def customer_change(request, edit_id=None):
    obj = models.Customer.objects.filter(pk=edit_id).first()
    form_obj = forms.CustomerForm(instance=obj)
    if request.method == 'POST':
        form_obj = forms.CustomerForm(request.POST, instance=obj)   # 有instance是修改数据，无则增加数据
        if form_obj.is_valid():
            form_obj.save()  
            return redirect(reverse('customer_list'))
    return render(request, 'customer_change.html', {'form_obj': form_obj, 'edit_id': edit_id})

```

### 公户与私户
什么是公户？  
​	客户没有绑定销售，就是公户  
什么是私户？  
​	客户绑定销售，就是某个销售的私户  

修改模板
增加私户路由
修改展示用户 路由
设置 sesion
写中间件

写注销  模板文件
    路由
    
公户和私户的转换

​	orm操作

### 模糊查询
利用Q
Q的两种用法  
`Q(qq__contains=query)   <==>   Q(('qq__contains',query))`

```python
    def search(self, query_list):
        query = self.request.GET.get('query', '')
        q = Q()
        q.connector = 'OR'
        # Q(qq__contains=query)   <==>   Q(('qq__contains',query))
        for i in query_list:
            q.children.append(Q(('{}__contains'.format(i), query)))
        return q

```

### 分页保留搜索条件

在创造分页的时候将本页面的参数与页码数加入分页URL参数中

```python
request.GET    # query：1    字典格式
request.GET.urlencode()   # 'query=1'   字符串格式
request.GET._mutable = True   # 可修改     
request.GET['page'] = 1  # query：1  page : 1 
request.GET.urlencode()   # 'query=1&pagr=1'

request.GET.copy()  # 深拷贝，可以修改
```

### 编辑后返回原页面
1. 客户展示页 -》 编辑  -》a标签 -》 URL   增加当前页面参数  
    1. 自定义simpletag，反向解析，增加参数
2. 编辑客户页提交后 ——》 customer_edit路由 ——》 视图函数   在重定向页面中增加当前页面参数
    1. 自定义函数，反向解析，增加当前页面参数

### 跟进记录列表，增加，编辑
增加、编辑 除去不属于该用户的信息，   
    所咨询的客户，必须是自己的用户  私户中的
    跟进人只能是自己
    

```python
# 选择框的数据
print(list(self.fields['customer'].choices))        
print(list(self.fields['customer'].widget.choices))

# choices字段，只有外键才有的，目前不清楚原理

# 内存中创建一个包含销售对象的ConsultRecord对象  数据库中没有该数据
obj = models.ConsultRecord(consultant=request.account)
obj.save()  # 新增   
  
# 编辑
obj = models.ConsultRecord.objects.get(id=1)
obj.note = ''
obj.save()   # 保存到数据库

obj = models.ConsultRecord(consultant=request.account)
form_obj = ConsultForm(instance=obj)

# 生成choices的数据 [] 中的元素是元组 （）第一个参数是数据库要保存的值  第二个参数是要显示的结果  
customer_choices = [(i.pk, str(i)) for i in self.instance.consultant.customers.all()]
customer_choices.insert(0, ('', '---------'))

# 修改choices的值
self.fields['customer'].choices = customer_choices

```


### 报名记录

```python
# 限制客户是当前的客户
self.fields['customer'].choices = [(self.instance.customer_id, str(self.instance.customer))]
# 限制客户可选的班级是记录中已报的班级
self.fields['enrolment_class'].choices = [(i.pk, str(i)) for i in self.instance.customer.class_list.all()]
```

### 解决公户转私户的问题
问题描述：
1. 两个用户同时抢同一批客户，第一个用户提交后，第二用户再提交，结果客户到了第二个用户里面。
2. 两个用户几乎同时抢同一批客户，将造成数据库中数据变脏


数据库中加锁：
```text
begin;   开始事务

select * from user where id=1 for update;    加锁

commit;   结束事务
```

django中加锁：

```
    with transaction.atomic():
        # 查询出数据加锁
        query_set = models.Customer.objects.filter(pk__in=pk, consultant__isnull=True).select_for_update()  # 加锁
        # 如果没有抢到
        if len(pk) != len(query_set):
            return HttpResponse('手慢了，没抢到哦!')
        query_set.update(consultant=self.request.account)

```

### 设置用户的客户数量上限
```text
    # 限制每个用户的最多客户数量
    if self.request.account.customers.all().count() + len(pk) > settings.MAX_ACCOUNT_NUM:
        return HttpResponse('已达拥有客户上限，无法再申请！')

```


### 班主任的功能

- 班级的管理	

   form的*/__all*__ 在前端的显示 {{ form_obj.non_field_errors.0 }}

- 课程记录的管理

- 学习记录的管理
      批量创建数据

    ```
        study_record_list = []
    for student in all_students:
        study_record_list.append(models.StudyRecord(course_record=course_record_obj, student=student))
    models.StudyRecord.objects.bulk_create(study_record_list)   # 批量创建数据
    
    ```

    ```


#### modelformset 
适用于对多个表单进行操作，字段可以用model中的表的字段来作为验证规则。
```
# 生成FormSet的类
FormSet = modelformset_factory(models.StudyRecord, StudyRecordForm, extra=0) 
# 查询的数据
all_study_record = models.StudyRecord.objects.filter(course_record_id=course_record_id)
# modelformset对象
form_obj = FormSet(queryset=all_study_record)

form_obj = FormSet(request.POST, queryset=all_study_record)
form_obj.is_valid()
form_obj.save()

# 错误提示
form_obj.errors
```



```
{{ form.instance }}   ——》   每一个数据  对应的对象
{{ form.instance.student }}    —— 》 值
{{ form.attendance }}		  —— 》  input框 select框

注意：
{{ form_obj.management_form }}     
每一行要有 {{ form.id }} 
```

