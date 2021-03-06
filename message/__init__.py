import importlib
from django.conf import settings

def send_message(to,name,subject,body):
    """
    短信、邮件、微信
    :param to: 接受者
    :param name: 接受者姓名
    :param subject: 主题
    :param body: 内容
    :return:
    """
    for cls_path in settings.MESSAGE_CLASSES:
        # cls_path是字符串
        module_path,class_name = cls_path.rsplit('.',maxsplit=1)
        m = importlib.import_module(module_path)  ##用字符串的方式导入模块
        obj = getattr(m,class_name)()  #导入类
        obj.send(subject,body,to,name,)