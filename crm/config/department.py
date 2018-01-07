#!usr/bin/env python
# -*- coding:utf-8 -*-
from stark.service import v1
class DepartmentConfig(v1.StarkConfig):
    list_display = ["title","code"]
    edit_link = ["title"]   #自定制链接，指定字段可编辑

    # 重写get_list_display(),因为父类有这个方法，如果这里不写就会继承父类的，写了就优先执行自己的
    def get_list_display(self):
        result = []

        result.extend(self.list_display)
        result.insert(0,v1.StarkConfig.checkbox)
        result.append(v1.StarkConfig.edit)
        result.append(v1.StarkConfig.delete)

        return result