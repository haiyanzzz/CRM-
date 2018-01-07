
'''
- 如果遇到类的约束，
    - 在Python中，有两种方式
        - 接口类，from abc import AbcMeta
        - 抛异常：NOTImplementedError异常
'''
# from abc import ABCMeta
# from abc import abstractmethod
#
# class BaseMessage(metaclass=ABCMeta):
#
#     @abstractmethod
#     def send(self,subject,body,to,name):
#         pass


class BaseMessage(object):
    def send(self, subject, body, to, name):
        raise NotImplementedError('未实现send方法')