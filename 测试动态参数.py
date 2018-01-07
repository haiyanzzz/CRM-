
#!usr/bin/env python
# -*- coding:utf-8 -*-
# def foo(x,y,**kwargs):
#     print(x,y)
#     print(kwargs) #{'c': 3, 'd': 4, 'f': 6} 吧多余的元素以字典的形式返回了
#     print(*kwargs) #输出c d f ，就是把字典打散了
#
# # foo(1,2,{"a":2})
# foo(1,7,k=2,c=3,d=4,f=6)

# def bar(x,y,z):
#      print(x,y,z)
# bar(1,2,3)
# bar(*['b','a','c']) #bar('b','a','c')
# bar(*'hel') #bar('h','e','l')
# bar(*{'a':1,'b':2,'c':3}) #bar('b','a','c')
# bar('b','a','c') #bar('b','a','c'# )


# def  Foo(**kwargs):
#     print(kwargs)
#     # print(*kwargs)
# # Foo(**{"id":3})
# Foo(**{"id":3})
# Foo(id=3,cc="dd",s=3)   #上面的和这个是一样的



import importlib
from django.conf import settings

MESSAGE_CLASSES = [
    'message.email.Email',
    'message.msg.Msg',
    'message.wx.WeChat',
    'message.dingding.DingDing',
]
for cls_path in MESSAGE_CLASSES:
    # cls_path是字符串
    module_path,class_name = cls_path.rsplit('.',maxsplit=1)
    print(module_path,class_name)
    m = importlib.import_module(module_path)  #用字符串的方式导入模块
    obj = getattr(m,class_name)()   #导入类
    print(obj)
