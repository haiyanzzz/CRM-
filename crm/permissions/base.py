#!usr/bin/env python
# -*- coding:utf-8 -*-
from stark.service import v1
class BasePermission(object):
    def get_show_add_btn(self):
        code_list = self.request.permission_code_url
        print(code_list,"0000000000000")
        if "add" in code_list:
            return True

    def get_edit_link(self):
        code_list = self.request.permission_code_url
        if "edit" in code_list:
            return super(BasePermission,self).get_edit_link()
        return []

    def get_list_display(self):
        code_list = self.request.permission_code_url
        data = []
        if self.list_display:
            data.extend(self.list_display)
            if 'del' in code_list:
                data.append(v1.StarkConfig.delete)
            data.insert(0, v1.StarkConfig.checkbox)
        return data