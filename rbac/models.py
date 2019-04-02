from django.db import models


class Menu(models.Model):
    """
    菜单表     一级菜单
    """
    title = models.CharField(max_length=32, verbose_name='名称')
    icon = models.CharField(max_length=32, null=True, blank=True, verbose_name='图标')
    weight = models.IntegerField(default=1, verbose_name='权重')

    def __str__(self):
        return self.title


class Permission(models.Model):
    """
    权限表
    可以做二级菜单的权限   menu 关联 菜单表
    不可以做菜单的权限    menu=null
    """
    url = models.CharField(max_length=108, verbose_name='权限')
    title = models.CharField(max_length=32, verbose_name='标题')
    menu = models.ForeignKey(to='Menu', null=True, blank=True, verbose_name='所属菜单')
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name='父权限')  # 自关联
    name = models.CharField(max_length=64, verbose_name='URL别名')

    def __str__(self):
        return self.title


# class Permission(models.Model):
#     """
#     权限表
#     可做菜单的权限    is_menu=True
#     不可做菜单的权限  is_menu=False
#     """
#     url = models.CharField(max_length=32, verbose_name='权限')
#     title = models.CharField(max_length=32, verbose_name='标题')
#     is_menu = models.BooleanField(default=False, verbose_name='是否是菜单')
#     icon = models.CharField(max_length=64, null=True, blank=True, verbose_name='图标')
#
#     def __str__(self):
#         return self.title


class Role(models.Model):
    """
    角色表
    """
    name = models.CharField(max_length=32, verbose_name='名称')
    permission = models.ManyToManyField(to='Permission', verbose_name='角色拥有的权限', blank=True)

    def __str__(self):
        return self.name


class User(models.Model):
    """
    用户表
    """
    # name = models.CharField(max_length=32, verbose_name='名称')
    # password = models.CharField(max_length=32, verbose_name='密码')
    role = models.ManyToManyField(to=Role, verbose_name='用户拥有的角色', blank=True)

    # def __str__(self):
    #     return self.name
    class Meta:
        abstract = True  # 数据库迁移时候不会生成表，用来做基类
