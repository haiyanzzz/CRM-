#!usr/bin/env python
# -*- coding:utf-8 -*-
from stark.service import v1
class ConsultRecordConfig(v1.StarkConfig):
    '''客户跟进记录'''
    def customer_display(self,obj=None,is_header=False):
        if is_header:
            return "所咨询客户"
        return obj.customer.name
    list_display = [customer_display,"consultant","date","note"]
    comb_filter = [
        v1.FilterOption("customer"),
    ]   #组合搜索默认不显示，但是却又筛选的功能

    def change_views(self, request,*args, **kwargs):
        customer = request.GET.get('customer')
        # session中获取当前用户ID
        current_login_user_id = 6
        ct = models.Customer.objects.filter(consultant=current_login_user_id, id=customer).count()
        if not ct:
            return HttpResponse('无权访问.')
        return super(ConsultRecordConfig,self).change_views(request, *args, **kwargs)