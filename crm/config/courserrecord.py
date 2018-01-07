from django.shortcuts import render,HttpResponse,redirect
from django.urls.base import reverse
from django.utils.safestring import mark_safe
from stark.service import v1
from crm import models
from django.conf.urls import url
class CourseRecordConfig(v1.StarkConfig):
    '''老师上课记录'''
    def extra_urls(self):
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name)
        score_url = [
            url(r'^(\d+)/score_list/$', self.wrap(self.score_list), name="%s_%s_score_list" % app_model_name),
        ]
        return score_url

    def score_list(self,request,record_id):
        '''
        :param request:
        :param record_id:  老师上课的记录id
        :return:
        '''
        if request.method=="GET":
            #方式一
            # study_record_list = models.StudyRecord.objects.filter(course_record_id=record_id)  #这一天上课的所有的学生的学习记录
            # score_choices = models.StudyRecord.score_choices
            # return render(request,"score_list.html",{"study_record_list":study_record_list,"score_choices":score_choices})

            #方式二：
            # 利用Form来做
            from django.forms import Form
            from django.forms import fields
            from django.forms import widgets
            # class SrudyForm(Form):
            #     score = fields.ChoiceField(choices=models.StudyRecord.score_choices)
            #     homework_note = fields.CharField(widget=widgets.Textarea())
            study_record_list = models.StudyRecord.objects.filter(course_record_id=record_id)
            print(study_record_list)
            data = []
            for obj in study_record_list:
                SrudyForm = type("SrudyForm",(Form,),{
                    "score_%s"%obj.id:fields.ChoiceField(choices=models.StudyRecord.score_choices),
                    "homework_note_%s"%obj.id:fields.CharField(widget=widgets.Textarea())
                })
                data.append({"obj":obj,"form":SrudyForm(initial={"score_%s"%obj.id:obj.score,"homework_note_%s"%obj.id:obj.homework_note})})
                print(data)
            return render(request, "score_list_update.html", {"data":data})
        else:
            # print(request.POST) #QueryDict
            data_dict={}
            '''
            构造这样的字典，目的是保存更新数据库里面的数据，字典的结构的
            {
                3:{"score":2,"homework_note":2}
                4:{"score":4,"homework_note":4}
            }
            '''
            for key,value in request.POST.items():
                # print(key,value)
                if key=="csrfmiddlewaretoken":
                    continue
                name,nid = key.rsplit("_",1)
                if nid in data_dict:
                    data_dict[nid][name] = value
                else:
                    data_dict[nid] = {name:value}
                print(data_dict)
            #构造完字典以后开始更新数据，当一点提交的时候，每个学生的成绩和评语应该默认显示，并保存到数据库
            for nid,update_dict in  data_dict.items():
                models.StudyRecord.objects.filter(id=nid).update(**update_dict)
            return redirect(request.path_info)
    def kaoqin(self,obj=None,is_header=False):
        if is_header:
            return "考勤"
        return mark_safe("<a href='/index/crm/studyrecord/?course_record=%s'>考勤管理</a>"%obj.pk)

    def luru_score(self,obj=None,is_header=False):
        if is_header:
            return "录入成绩"
        url = reverse('stark:crm_courserecord_score_list', args=(obj.pk,))
        return mark_safe("<a href='%s'>录入成绩</a>" % (url))
    list_display = ["class_obj","day_num",kaoqin,"date",luru_score]
    edit_link = ["class_obj"]

    def mutil_init(self,request):
        '''初始化的目的是为每一个同学创建记录'''
        pk_list = request.POST.getlist("pk")  #['1', '2'] 用户发过来的上课记录的id
        record_list = models.CourseRecord.objects.filter(id__in=pk_list)  #数据库中查出的上课记录对象
        for record in record_list:
            print(type(record),"record")  #python(6期) day2 对象
            exists = models.StudyRecord.objects.filter(course_record=record).exists()
            if exists:
                continue
            student_list = models.Student.objects.filter(class_list=record.class_obj)  #查出这个班的所有的学生
            bluk_list = []
            for stu in student_list:
                bluk_list.append(models.StudyRecord(student=stu,course_record=record))
            models.StudyRecord.objects.bulk_create(bluk_list)

    mutil_init.short_desc = "学生初始化"
    actions = [mutil_init]
    show_actions = True
    show_add_btn = False