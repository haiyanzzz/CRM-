#!usr/bin/env python
# -*- coding:utf-8 -*-
l = ["zhy",666]
l.extend(["edit","sdd"])
# print(l)   #['zhy', 666, 'edit', 'sdd']
l.append(["bb","aa"])
# print(l)  #['zhy', 666, 'edit', 'sdd', ['bb', 'aa']]
# append是往元素的最后添加，extend是打开列表扩展

l = ["-status","xx"]
print(*l)