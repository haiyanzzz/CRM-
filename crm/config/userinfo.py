#!usr/bin/env python
# -*- coding:utf-8 -*-
from stark.service import v1
from django.shortcuts import render,redirect
from django.forms import ModelForm
from crm import models
class UserInfoConfig(v1.StarkConfig):
    edit_link = ["name"]

    def depart_dispaly(self,obj=None,is_header=False):
        if is_header:
            return "所属部门"
        return obj.depart.title

    def get_model_form_class(self):
        '''自定义ModelForm'''
        class MyModelForm(ModelForm):
            class Meta:
                model = models.UserInfo
                fields = "__all__"
                error_messages = {
                    "name":{"required":"姓名不能为空"},
                    "username":{"required":"用户名不能为空"},
                    "password":{"required":"密码不能为空"},
                    "email":{"required":"邮箱不能为空","invalid":"邮箱格式不正确"},
                    "depart":{"required":"用户名不能不选",},
                }
        return MyModelForm

    list_display = ["name","username","email",depart_dispaly]

    comb_filter = [
        v1.FilterOption("depart",val_func_name=lambda x: x.code,),
    ]  #分组搜索

    def delete_view(self, request,nid, *args, **kwargs):
        '''重写视图函数'''
        if request.method=="GET":
            return render(request, "stark/delete_view.html", {"quxiao_url":self.get_list_url()})
        else:
            self.model_class.objects.filter(pk=nid).delete()
            return redirect(self.get_list_url())