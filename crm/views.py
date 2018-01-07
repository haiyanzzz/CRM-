from django.http import StreamingHttpResponse
from django.shortcuts import render,redirect,HttpResponse
from django.forms import Form
from django.forms import fields
from django.forms import widgets
from rbac import  models
from rbac.service.init_permission import init_permission
# Create your views here.
class User_login_Form(Form):
    name = fields.CharField(required=True,error_messages={
        "required":"用户名不能为空"
    },
            label="用户名"
            ,widget=widgets.TextInput(attrs={"placeholder":"username","class":"form-control"}))

    password = fields.CharField(required=True, error_messages={
        "required": "密码不能为空"
    },
    label="密码",
   widget=widgets.PasswordInput(attrs={"placeholder": "password", "class": "form-control"}))

def login(request):
    if request.method=="GET":
        form = User_login_Form()
        return render(request,"user_login.html",{"form":form})
    else:
        form = User_login_Form(request.POST)
        if form.is_valid():
            user = models.User.objects.filter(**form.cleaned_data).first()
            print(user.userinfo.id,"uid")
            print(user.userinfo.name,"name")
            if user:
                #表示已登录
                request.session["user_info"] = {"id":user.id,"name":user.userinfo.name,"uid":user.userinfo.id}
                #权限写入session
                init_permission(user,request)
                return redirect("/loginindex/")
        return render(request,"user_login.html",{"form":form})



from urllib.request import quote
def load_view(request):
    '''下载文件的第二种方式'''
    the_file_name = 'static/xxx.xlsx'   #模板文件
    def file_iterator(file_name, chunk_size=512):
        with open(file_name, 'rb') as  f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(quote(the_file_name.rsplit('/', 1)[1]))
    print(response['Content-Disposition'])
    return response


def loginindex(request):
    return render(request,"loginindex.html")