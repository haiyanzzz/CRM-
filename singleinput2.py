#!usr/bin/env python
# -*- coding:utf-8 -*-
import redis
from crm import models
#链接方式一
conn = redis.Redis(host="192.168.20.100",port=6379,password="") #链接redis
#链接方式二:推荐
# POOL = redis.ConnectionPool(host="47.93.4.168",port=6379,password="")
# COON = redis.Redis(connection_pool=POOL)
class AutoSale(object):
    """
    目的：在系统自动分配客户时，提供一个销售ID
    接口：
        get_sale_id 返回销售ID
        fetch_user 初始化
        reset 重置队列
        rollback 将取出的销售ID放回到队列中
    
    """
    SALE_ID_LIST = "sale_id_list"
    SALE_ID_LIST_ORIGIN = "sale_id_list_origin"
    @classmethod
    def fetch_user(cls):
        '''初始化'''
        sales = models.SaleRank.objects.all().order_by("-weight")
        max_num = models.SaleRank.objects.all().order_by("-num").first()
        sale_id_list =[]
        for i in range(max_num):   #[1,2,3,4,5,6,7,8,9]
            for sale in sales:
                if sale.num > i:  #10,3,4
                    sale_id_list.append(sale.id)
        print(sale_id_list)

        if sale_id_list:
            #如果有值，放到redis列表里面去
            conn.rpush("sale_id_list",*sale_id_list)
            conn.rpush("sale_id_list_origin",*sale_id_list)   #原数据
            return True
        return False

    @classmethod
    def get_sale_id(cls):
        '''预留的接口，调用时返回一个sale_id'''
        #查看原来的数据是否存在
        sale_id_origin_count = conn.llen("sale_id_list_origin")
        if not sale_id_origin_count:
            #如果不存在，重新去数据库获取
            status = cls.fetch_user()
            if not status:  #如果没有取到值，就返回None
                return None
        sale_id = conn.lpop("sale_id_list")
        if sale_id:
            return sale_id

        reset = conn.get("sale_id_reset")
        #如果得到值了，说明要重置
        if reset:
            conn.delete("sale_id_list_origin")
            #重新从数据库获取
            status = cls.fetch_user()
            if not status:
                return None
            conn.delete("sale_id_reset")
            return conn.lpop("sale_id_list")
        else:
            ct = conn.llen('sale_id_list_origin')
            for i in range(ct):
                v = conn.lindex('sale_id_list_origin', i)
                conn.rpush('sale_id_list', v)
            return conn.lpop('sale_id_list')

    @classmethod
    def reset(cls):
        conn.set("sale_id_reset",1) #随便给设置一个值，说明他有值

    @classmethod
    def rollback(cls,sid):
        conn.lpush("sale_id_list",sid)