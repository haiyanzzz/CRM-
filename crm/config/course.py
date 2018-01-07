from stark.service import v1
class CourseConfig(v1.StarkConfig):
    list_display = ["name"]
    edit_link = ["name"]
    show_actions =True  #显示actions

    def mutil_delete(self,request):
        if request.method =="POST":
            pk_list = request.POST.getlist("pk")
            # print(pk_list,"000")
            self.model_class.objects.filter(id__in=pk_list).delete()

    mutil_delete.short_desc = "批量删除"
    def init_func(self):
        pass
    init_func.short_desc = "初始化"
    actions = [mutil_delete,init_func]   #actios操作


    search_fields = ["name__contains"]   #按照name搜索
    show_search_form = True