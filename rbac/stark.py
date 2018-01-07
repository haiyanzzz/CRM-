#!usr/bin/env python
# -*- coding:utf-8 -*-
from stark.service import v1
from rbac import models
class UserConfig(v1.StarkConfig):
    list_display = ["id","name","email"]
    edit_link = ["name"]
v1.site.register(models.User,UserConfig)

class RoleConfig(v1.StarkConfig):
    list_display = ["id","title"]
    edit_link = ["title"]
v1.site.register(models.Role,RoleConfig)

class PermissionConfig(v1.StarkConfig):
    list_display = ["id","title","url","codes","menu_gp"]
    edit_link = ["url"]
v1.site.register(models.Permission,PermissionConfig)

class MenuConfig(v1.StarkConfig):
    list_display = ['id', 'caption']
    edit_link = ['caption']
v1.site.register(models.Menu,MenuConfig)

class GroupConfig(v1.StarkConfig):
    list_display = ['id', 'title', 'menu']
    edit_link = ['title']
v1.site.register(models.Group,GroupConfig)