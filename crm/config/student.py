from audioop import reverse
import json
from django.shortcuts import render,HttpResponse,redirect
from django.urls.base import reverse
from django.utils.safestring import mark_safe
from stark.service import v1
from crm import models
from django.conf.urls import url
class StudentConfig(v1.StarkConfig):
    def extra_urls(self):
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name)
        score_url = [
            url(r'^(\d+)/sv/$', self.wrap(self.score_view), name="%s_%s_sv" % app_model_name),
            url(r'^chart/$', self.wrap(self.score_chart), name="%s_%s_chart" % app_model_name),
        ]
        return score_url
    def score_chart(self,request):
        ret = {"status":False,"data":None,"msg":None}
        try:
            cid = request.GET.get("cid")
            sid = request.GET.get("sid")
            record_list = models.StudyRecord.objects.filter(student_id=sid,course_record__class_obj_id=cid).order_by("course_record__id")
            data = [
                # ['day1', 24.25],
                # ['day2', 23.50],
                # ['day3', 21.51],
                # ['day4', 16.78],
                # ['day5', 16.06],
                # ['day6', 15.20]
            ]
            for item in record_list:
                day = "day%s"%item.course_record.day_num
                data.append([day,item.score])
                ret["status"] = True
                ret["data"] = data
        except Exception as e:
            ret["msg"] = "获取失败"
        return HttpResponse(json.dumps(ret))
    def score_view(self, request,sid):
        print(sid)
        obj = models.Student.objects.filter(id=sid).first()
        if not obj:
            return "查无此人"
        class_list = obj.class_list.all()   #拿到这个学生所关联的班级对象
        print(class_list,"class_list")   #[<ClassList: python(6期)>, <ClassList: Java(3期)>, <ClassList: python(4期)>]>
        return render(request, "score_view.html", {"class_list":class_list, "sid":sid})


    def display_scores(self,obj=None,is_header=False):
        if is_header:
            return "查看成绩"
        surls = reverse("stark:crm_student_sv", args=(obj.pk,))
        return mark_safe("<a href='%s'>点击查看</a>" % surls)



    list_display = ["customer", "username", display_scores]