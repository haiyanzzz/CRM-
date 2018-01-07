from stark.service import v1
from crm import models
class StudyRecordConfig(v1.StarkConfig):
    '''学生学习记录'''
    def display_record(self,obj=None,is_header=False):
        if is_header:
            return "出勤"
        return obj.get_record_display()
    list_display = ["course_record","student",display_record,]
    edit_link = ["student"]
    comb_filter = [
        v1.FilterOption("course_record")  #按课程组合搜索
    ]
    def checked(self,request):
        pk_list = request.POST.getlist("pk")
        models.StudyRecord.objects.filter(id__in=pk_list).update(record="checked")
    checked.short_desc = "已签到"

    def vacate(self,request):
        pk_list = request.POST.getlist("pk")
        models.StudyRecord.objects.filter(id__in=pk_list).update(record="vacate")
    vacate.short_desc = "请假"

    def late(self,request):
        pk_list = request.POST.getlist("pk")
        models.StudyRecord.objects.filter(id__in=pk_list).update(record="late")
    late.short_desc = "迟到"

    def noshow(self,request):
        pk_list = request.POST.getlist("pk")
        models.StudyRecord.objects.filter(id__in=pk_list).update(record="noshow")
    noshow.short_desc = "缺勤"

    def leave_early(self,request):
        pk_list = request.POST.getlist("pk")
        models.StudyRecord.objects.filter(id__in=pk_list).update(record="leave_early")
    leave_early.short_desc = "早退"

    actions = [checked,vacate,late,noshow,leave_early]
    show_actions = True