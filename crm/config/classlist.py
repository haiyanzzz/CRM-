from stark.service import v1
class ClassListConfig(v1.StarkConfig):
    def teachers_display(self,obj=None,is_header=False):
        if is_header:
            return "任教老师"
        user_list = obj.teachers.all()
        html = []
        for i in user_list:
            html.append(i.name)
        return ','.join(html)

    def display_graduate_date(self,obj=None,is_header=False):
        if is_header:
            return "结业日期"
        return '' if not obj.graduate_date else obj.graduate_date

    def  display_memo(self,obj=None,is_header=False):
        if is_header:
            return "说明"
        return '' if not obj.memo else obj.memo

    def course_semester(self,obj=None,is_header=False):
        if is_header:
            return "课程（班级）"
        return "%s(%s期)"%(obj.course,obj.semester)

    #列举这个班级的人数
    def num(self,obj=None,is_header=False):
        if is_header:
            return "人数"
        # print(obj.student_set.all().count())
        return obj.student_set.all().count()
    list_display = ["school",course_semester,num,"price","start_date",display_graduate_date,display_memo,teachers_display,"tutor"]
    edit_link = ["school","tutor"]
    # ############## 作业2：组合搜索（校区、课程） #############

    comb_filter = [
        v1.FilterOption("school"),
        v1.FilterOption("course")
    ]
    show_comb_filter = True
    # ############## 作业3：popup增加时，是否将新增的数据显示到页面中（获取条件） #############
    # 查到limit_choices_to来做
    # new_obj._meta.related_objects  #找到这个对象所有关联的对象，也就是Fk,M2M
    # 1、当点击popup的时候，在url上带上model_name=classlist&related_name=classes
    # 2、后台拿到这两个值，作比较。如果一样就页面才显示