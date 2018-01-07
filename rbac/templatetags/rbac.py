#!usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf import settings
import re
from django.template import Library
register = Library()
@register.inclusion_tag("rbac/xxxx.html")
def menu_html(request):
    """
       去Session中获取菜单相关信息，匹配当前URL，生成菜单
       :param request:
       :return:
       """
    menu_list = request.session.get(settings.PERMISSION_MENU_KEY)
    current_url = request.path_info
    menu_dict = {}
    for item in menu_list:
        # 循环找到可以作为菜单的权限,组内菜单id为null的
        if not item["menu_gp_id"]:
            menu_dict[item["id"]] = item
    # 正则匹配添加active
    for item in menu_list:
        regex = "^{0}$".format(item["url"])
        if re.match(regex, current_url):
            # 匹配成功在根据id去判断,如果菜单id有值就不是菜单，则去找它的值对应的id,添加active
            # ，为null时就是菜单,直接给自己添加一个active
            if not item["menu_gp_id"]:  #是菜单
                menu_dict[item["id"]]["active"] = True
            else:
                menu_dict[item["menu_gp_id"]]["active"] = True

    result = {}
    for item in menu_dict.values():
        active = item.get("active")
        menu_id = item["menu_id"]
        if menu_id in result:
            result[menu_id]["children"].append({'title': item['title'], 'url': item['url'], 'active': active})
            if active:
                result[menu_id]["active"] = True
        else:
            result[menu_id] = {
                'menu_id': item['menu_id'],
                'menu_title': item['menu_title'],
                'active': active,
                'children': [
                    {'title': item['title'], 'url': item['url'], 'active': active}
                ]
            }
    print("result",result)
    return {"menu_dict":result}