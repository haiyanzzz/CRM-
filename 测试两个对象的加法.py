#!usr/bin/env python
# -*- coding:utf-8 -*-
class Foo(object):
    def __init__(self,age):
        self.age = age

    def __add__(self, other):
        return self.age+other.age

obj1 = Foo(21)
obj2 = Foo(20)
obj3 = obj1+obj2
print(obj3)