#!usr/bin/env python
# -*- coding:utf-8 -*-
from django.db.models import Max

from crm import models
class AutoSale:
    '''分配客户的类'''
    users = None   #[1,2,4,1,2,5,]
    iter_users = None  # 目的是弄一个迭代器  iter([1,2,4,1,2,5,])
    reset_status = False
    rollback_list = []
    @classmethod
    def fetch_users(cls):
        sales = models.SaleRank.objects.all().order_by("-weight")  #根据权重从大到小的排序
        #方式一
        # num_obj = models.SaleRank.objects.all().order_by("-num").first()
        # v = []
        # for i in range(num_obj.num):   #权重最大的数
        #     for obj in sales:
        #         if obj.num>i:
        #             v.append(obj.id)
        # print(v)
        #方式二
        # print(sales,"1111")
        #拿到的是一个列表，[obj(销售id,,个数),obj(销售id,,个数)obj,obj(销售id,,个数)obj]
        sale_id_list = []
        count = 0
        while True:
            flag = False
            for row in sales:
                if row.num > count:
                    sale_id_list.append(row.user.id)
                    flag = True
            count += 1
            if not flag:
                break
        cls.users = sale_id_list
        # 吧拿到的数据按照销售的权重和数量分配销售生成这样的结构
        '''
        分配表：
			姓名    分配数量    权重
			番禺       3		  7
			依依       3		  6
			富贵       2 		  9
			啧啧       10	      1
        先按照权重来分配，并排序：
         富贵       2 		  
         番禺       3		  
         依依       3		  
         啧啧       10
        '''
        # v=[富贵,番禺,依依,啧啧,富贵,番禺,依依,啧啧,番禺,依依,啧啧,啧啧,啧啧,啧啧,啧啧]


    @classmethod
    def get_sale_id(cls):
       if cls.rollback_list:
           return cls.rollback_list.pop()

       if not cls.users:
           #如果没有数据，吧数据库的数据拿过来
            cls.fetch_users()

       if not cls.users:
           return None

       if not cls.iter_users:
           cls.iter_users = iter(cls.users)

       try:
            user_id = next(cls.iter_users)
       except StopIteration as e:
           # 一轮执行完的时候再重置
           if cls.reset_status:  # 如果是True的话就 重新在从数据库里面查一下，并且在吧cls.reset_status设置为False
               cls.fetch_users()
               cls.reset_status = False

           cls.iter_users = iter(cls.users)
           user_id = cls.get_sale_id()
       return user_id

    @classmethod
    def reset(cls):
        # 老大觉得谁表现好给增加了销售数num, 那内存里面的users也的更新。需要重置一下
        cls.reset_status = True

    @classmethod
    def rollback(cls,nid):
        '''在后台得到销售id的时候，有可能由于网络原因啥的，就会出错，生成器只能取值不能回归，所以自定义一个
        回滚函数，用一个空列表存起来，如果这个列表不空，就把值取出来，在重复一下原来的操作
        '''
        cls.rollback_list.insert(0,nid)  #nid  销售id