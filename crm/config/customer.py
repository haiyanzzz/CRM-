#!usr/bin/env python
# -*- coding:utf-8 -*-
from django.db.models import Q
from django.shortcuts import render,HttpResponse,redirect
from django.utils.safestring import mark_safe
from stark.service import v1
from crm import models
from django.conf.urls import url
from django.db import transaction
import datetime
from django.forms import ModelForm
import message
from singleinput2 import AutoSale
from crm.permissions.customer import CustomerPermission

class SingleModelForm(ModelForm):
    class Meta:
        model = models.Customer
        exclude = ["status","consultant","last_consult_date","recv_date"]  #除这些字段以外的所有字段


class CustomerConfig(CustomerPermission,v1.StarkConfig):
    order_by = ["-status"]
    def display_gender(self,obj=None,is_header=False):
        if is_header:
            return "性别"
        return obj.get_gender_display()
    def display_education(self,obj=None,is_header=False):
        if is_header:
            return "学历"
        return obj.get_education_display()

    def display_status(self, obj=None, is_header=False):
        if is_header:
            return '状态'
        return obj.get_status_display()
    def recode(self, obj=None, is_header=False):
        if is_header:
            return "跟进记录"
        return mark_safe("<a href='/index/crm/consultrecord/?customer=%s'>查看跟进记录</a>" %(obj.pk,))

    def display_course(self,obj=None, is_header=False):
        if is_header:
            return "咨询课程"
        course_list = obj.course.all()
        html = []
        for item in course_list:
            temp = "<a style='display:inline-block;padding:3px 5px;border:1px solid blue;margin:2px;' href='/index/crm/customer/%s/%s/dc/'>%s X</a>" %(obj.pk,item.pk,item.name)
            html.append(temp)
        return "".join(html)

    def extra_urls(self):
        # 由于没有路径，我们可以额外的增加一个路径,重新走一个delete_course视图
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name)
        urlpatterns =[
            url(r'^(\d+)/(\d+)/dc/$', self.wrap(self.delete_course), name="%s_%s_delete" % app_model_name),
            url(r'^public/$', self.wrap(self.public_view), name="%s_%s_public_view" % app_model_name),   #公共的客户
            url(r'^(\d+)/competition/$', self.wrap(self.competition_view), name="%s_%s_competition_view" % app_model_name),  #对公共的客户实现抢单，变成自己的客户
            url(r'^user/$', self.wrap(self.user_view), name="%s_%s_user_view" % app_model_name) ,  #我的客户
            url(r'^single/$', self.wrap(self.single_view), name="%s_%s_single_view" % app_model_name),   #市场部或者运营部单条录入客户数据
            url(r'^mutil/$', self.wrap(self.mutil_view), name="%s_%s_mutil_view" % app_model_name)   #市场部或者运营部单条录入客户数据

        ]
        return urlpatterns

    # ===============路由对应的视图函数===================
    def delete_course(self, request,customer_id,course_id):
        '''
        删除当前用户感兴趣的课程
        :param request:
        :param customer_id:
        :param course_id:
        :return:
        '''
        customer_obj = self.model_class.objects.filter(pk=customer_id).first()
        customer_obj.course.remove(course_id)
        return redirect(self.get_list_url())

    def public_view(self,request):
        '''
        公共客户资源
        :param request:
        :return:
        '''
        current_user_id = 2
        #条件：未报名并且（15天未成单（当前时间-15>接课时间）or 3天未跟进（当前时间-3天>最后跟进时间）  Q对象）
        import datetime
        no_deal = datetime.datetime.now().date()-datetime.timedelta(days=15)
        no_follow = datetime.datetime.now().date()-datetime.timedelta(days=3)
        # Q查询方式一：
        customer_list = models.Customer.objects.filter(Q(recv_date__lt=no_deal)|Q(last_consult_date__lt=no_follow),status=2)
        print(customer_list)
        # Q查询方式二：
        # con = Q()
        # q1 = Q()
        # q1.children.append(("recv_date__lt",no_deal))
        # q2 = Q()
        # q2.children.append(("last_consult_date__lt",no_follow))
        # q3 = Q()
        # q3.children.append(("status",2))
        # con.add(q1,"OR")
        # con.add(q2,"OR")
        # con.add(q3,"AND")
        # customer_list = models.Customer.objects.filter(con)
        return render(request, "public_view.html", {"customer_list":customer_list, "current_user_id":current_user_id})

    def competition_view(self,request,cid):
        '''对公共的客户实现抢单，变成自己的客户'''
        #修改客户表
            # 必须原顾问不是自己  :可用exclude方法排除
            # 状态必须是未报名
            # 3/15天
        import datetime
        current_user_id = 6
        no_deal = datetime.datetime.now().date()-datetime.timedelta(days=15)
        no_follow = datetime.datetime.now().date()-datetime.timedelta(days=3)
        current_time = datetime.datetime.now().date()
        row_count = models.Customer.objects.filter(Q(recv_date__lt=no_deal)|Q(last_consult_date__lt=no_follow),status=2,id=cid).exclude(consultant_id=current_user_id).update(consultant_id=current_user_id,recv_date=current_time,last_consult_date=current_time)
        if not row_count:   #对前端伪造发来的数据进行验证
            #在分配表中创建一条数据
            return HttpResponse("无权抢单")
        #在分配表中创建一条数据
        models.CustomerDistribution.objects.create(user_id=current_user_id,customer_id=cid,ctime=current_time)
        return HttpResponse("抢单成功")

    def user_view(self,request):
        '''当前登录用户的所有客户'''
        #去session中获取当前用户的id,我先在这里假设一下
        current_user_id = 2
        #查看当前用户的所有客户列表并且按照状态排序一下
        customer_list = models.CustomerDistribution.objects.filter(user_id=current_user_id).order_by("status")
        return render(request, "user_view.html", {'customer_list':customer_list})

    def single_view(self,request):
        if request.method =="GET":
            form = SingleModelForm()
            return render(request, "single_view.html", {"form":form})
        else:
            form = SingleModelForm(request.POST)
            if form.is_valid():
                # exclude = ["status", "consultant", "last_consult_date", "recv_date"]
                print(form.cleaned_data)
                """客户表新增数据：
                     - 获取该分配的课程顾问id
                     - 当前时间
                 客户分配表中新增数据
                     - 获取新创建的客户ID
                     - 顾问ID
             """

                # 方式一
                sale_id = AutoSale.get_sale_id() #获取该分配的销售id
                if not sale_id:
                    return HttpResponse("无销售顾问 ，无法进行自动分配")
                ctime = datetime.datetime.now().date()
                try:

                    with transaction.atomic():
                        print(111)
                        #创建客户表
                        #由于页面上没有这个值，所以数据库里面的值没有添加上，
                        # save保存会把所有的都保存。如果不设置值就会报错。所以，可以通过这种方式去做。额外的增加一条数据
                        form.instance.consultant_id = sale_id
                        form.instance.recv_date = ctime
                        form.instance.last_consult_date = ctime
                        customer_obj = form.save()
                        #创建客户分配表
                        models.CustomerDistribution.objects.create(user_id=sale_id,customer=customer_obj,ctime=ctime)
                    # 方式二：
                    # with transaction.atomic():
                    #     sale_id = Input_information.get_sale_id()
                    #     ctime = datetime.datetime.now().date()
                    #     course = form.cleaned_data.pop('course')
                    #     customer_obj = models.Customer.objects.create(**form.cleaned_data, consultant_id=sale_id,
                    #                                                   recv_date=ctime)
                    #     customer_obj.course.add(*course)
                    #     models.CustomerDistribution.objects.create(user_id=sale_id, customer=customer_obj, ctime=ctime)

                    #发送消息
                    message.send_message('2533916647@qq.com', 'dsfdfd', '你好', '这是真的')
                except Exception as e:
                    AutoSale.rollback(sale_id)
                    return HttpResponse("录入异常")
                return HttpResponse("录入数据成功")
            else:
                return render(request, "single_view.html", {"form":form})

    def mutil_view(self,request):
        if request.method=="GET":
            return render(request, "mutil_view.html")
        else:
            from django.core.files.uploadedfile import InMemoryUploadedFile
            file_obj = request.FILES.get("elfile")
            # print(type(file_obj))   #classs InMemoryUploadedFile
            # with open("xxx.xlsx","wb") as f :
            #     for line in file_obj:
            #         f.write(line)
            maps = {
                0:"qq",
                1:"name",
                2:"gender",
                3:"education",
                4:"graduation_school",
                5:"major",
                6:"experience",
                7:"work_status",
                8:"salary",
                9:"referral_from_id",
                10:"course",
                11:"date",
            }
            import xlrd
            from  io import  BytesIO
            f = BytesIO()
            for chunk in file_obj:
                f.write(chunk)
            workbook = xlrd.open_workbook(file_contents=f.getvalue())
            sheet_names = workbook.sheet_names()   #所有sheet的名字
            sheet = workbook.sheet_by_index(0)   #按照索引取值
            # print(sheet.nrows)
            row_dict = {}
            for index in range(1,sheet.nrows):  #所有的行
                sale_id = AutoSale.get_sale_id()  # 获取销售id
                print(sale_id, "aaaa")
                if not sale_id:
                    return HttpResponse("无销售顾问 ，无法进行自动分配")
                ctime = datetime.datetime.now().date()

                row = sheet.row(index)   #拿到的每一行的数据是一个列表，那么怎么变成字典呢？[text:'haiyan', number:34324.0]
                print(row)

                for i in range(len(maps)):
                    key = maps[i]
                    cell = row[i]
                    row_dict[key] = cell.value
                print(row_dict)  #{'name': 'haiyan', 'qq': 34324.0}
                # #拿到字典数据以后，现在就可以录入数据了
                # try:
                #     with transaction.atomic():
                #         row_dict["consultant_id"] = int(sale_id.decode("utf_8"))
                #         row_dict["last_consult_date"] = ctime
                #         row_dict["recv_date"] = ctime
                #         course_list = []
                #         course_list.extend(row_dict.pop("course").split(","))
                #         customer_obj = models.Customer.objects.create(**row_dict)#录入客户表
                #         customer_obj.course = course_list
                #         print(course_list,"xxxx")
                #         models.CustomerDistribution.objects.create(user=sale_id,customer=customer_obj,ctime=ctime)#录入分配表
                # #         #由于数据库的字段可能和表里面的字段不一致，我们可以制定一个模板，让用户都按照制定的这个模板存数据，让用户去下载文件
                # except Exception as e:
                #     AutoSale.rollback(sale_id)
                #     print(e)
                #     return HttpResponse("录入异常")
            return HttpResponse("录入数据成功")

    def multi_view(self, request):
        """
        批量导入
        :param request:
        :return:
        """
        if request.method == 'GET':
            return render(request, 'mutil_view.html')
        else:
            file_obj = request.FILES.get('exfile')
            field_map = {
                'qq': 'QQ号',
                'name': '学生姓名',
                'gender': '性别',
                'education': '学历',
                'graduation_school': '毕业学校',
                'major': '所学专业',
                'experience': '工作经验',
                'work_status': '职业状态',
                'company': '目前就职公司',
                'salary': '当前薪资',
                'source': '客户来源',
                'course': '咨询课程',
            }

            import xlrd
            wb = xlrd.open_workbook(filename=None, file_contents=file_obj.read())  # 从内存中读取文件
            sheet = wb.sheet_by_index(0)
            # 验证表头
            header_list = [str(x.value).strip() for x in sheet.row(0)]
            if list(field_map.values()) != header_list:
                return HttpResponse('表头不正确，请重新下载模板')

            # 结构化数据
            temp_list = []
            for index in range(1, sheet.nrows):
                row = sheet.row(index)
                temp = {}
                for i in range(len(field_map.keys())):
                    temp[list(field_map.keys())[i]] = str(row[i].value).strip()
                temp_list.append(temp)

            # 校验数据
            error_msg_list = []
            for num, row in enumerate(temp_list, 1):
                choice_list = ['gender', 'education', 'experience', 'work_status', 'source']
                for field in choice_list:
                    if row[field] not in [x[1] for x in getattr(models.Customer, field + '_choices')]:
                        error_msg_list.append('第%s行%s填写有误' % (num, field_map[field]))
                course_list = str(row['course']).split(',')
                if models.Course.objects.filter(name__in=course_list).count() <= 0:
                    error_msg_list.append('第%s行%s填写有误' % (num, field_map['course']))
            if error_msg_list:
                return HttpResponse('<br/>'.join(error_msg_list))

            # 转换数据并录入
            for row in temp_list:
                row['qq'].rsplit('.0')
                row['gender'] = [x[0] for x in models.Customer.gender_choices if x[1] == row['gender']][0]
                row['education'] = [x[0] for x in models.Customer.education_choices if x[1] == row['education']][0]
                row['experience'] = [x[0] for x in models.Customer.experience_choices if x[1] == row['experience']][0]
                row['work_status'] = [x[0] for x in models.Customer.work_status_choices if x[1] == row['work_status']][0]
                row['source'] = [x[0] for x in models.Customer.source_choices if x[1] == row['source']][0]
                row['consultant_id'] = 6  # 自动获取ID
                course_list = str(row['course']).split(',')
                row['course'] = [x[0] for x in models.Course.objects.filter(name__in=course_list).values_list('id')]
                course_list = row.pop('course')
                obj = models.Customer.objects.create(**row)  # 录入客户表
                obj.course.add(*course_list)  # 绑定课程
                models.CustomerDistribution.objects.create(user_id=obj.consultant_id, customer_id=obj.id

                                                           )  # 录入客户分配表
            return HttpResponse('上传成功')

    list_display = ["qq","name","graduation_school",display_course,display_gender,display_status,display_education,recode]
    edit_link = ["name","graduation_school"]
    search_fields = ["name__contains"]
    show_search_form = True

    show_actions = True
    comb_filter = [
        v1.FilterOption("gender",is_choice=True),
        v1.FilterOption("education",is_choice=True),
        v1.FilterOption("experience",is_choice=True),
        v1.FilterOption("source",is_choice=True),
        v1.FilterOption("status",is_choice=True),
    ]

    show_comb_filter = True