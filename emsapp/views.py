import os, random, string, uuid
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse, JsonResponse, response
from django.shortcuts import render, redirect
from captcha.image import ImageCaptcha
from emsapp.models import User, Staff


# 登陆页面
def login1(request):
    name = request.COOKIES.get('username')
    pwd = request.COOKIES.get('userpwd')
    if name:
        name = name.encode('latin-1').decode('utf-8')
    req = User.objects.filter(name=name, user_pwd=pwd)
    if req:
        request.session['login'] = 'ok'
        return redirect("emsapp:emplist_logic")
    return render(request, 'emsapp/login.html')


# 登陆
def login(request):
    username = request.POST.get("name")
    userpwd = request.POST.get("pwd")
    rem = request.POST.get("remember")
    res = User.objects.filter(user_name=username, user_pwd=userpwd)
    if res:
        # 设置session
        request.session['login'] = True
        resp = JsonResponse({"error": 0, "msg": "登陆成功"})
        if rem:
            resp.set_cookie('username', username.encode("utf-8").decode('latin-1'), max_age=7 * 24 * 3600)
            resp.set_cookie('userpwd', userpwd, max_age=7 * 24 * 3600)
        # 使用ajax局部更新
        return resp
    return JsonResponse({"error": 1, "msg": "用户名或密码错误"})


# 注册
def regist(request):
    return render(request, 'emsapp/regist.html')


# 验证码生成
def getCaptcha(request):
    image = ImageCaptcha()
    code = random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits, 4)
    # 拼接字符,通过session传递验证码
    random_code = ''.join(code)
    request.session['code'] = random_code
    data = image.generate(random_code)
    return HttpResponse(data, 'image/png')


# 注册逻辑
def regist_logic(request):
    username = request.POST.get('username')
    password = request.POST.get('pwd')
    name = request.POST.get('name')
    sex = request.POST.get('sex')
    code = request.session['code']
    captcha = request.POST.get('captcha')
    print(captcha, name, type(username))
    try:
        with transaction.atomic():
            if username == '' or password == '' or name == '':
                10 / 0
            if captcha.lower() == code.lower():
                print(captcha.lower(), code.lower())
                res = User.objects.filter(user_name=username)
                if res:
                    return HttpResponse('user_have')
                else:
                    User.objects.create(user_name=username, user_pwd=password, name=name, sex=sex)
                    return HttpResponse('ok')
            else:
                return HttpResponse('error')
    except Exception as e:
        print(e)
        return HttpResponse("wrong")


# 主页逻辑
def emplist_logic(request):
    staff = Staff.objects.all()
    paginator = Paginator(staff, per_page=3)
    numbers = request.session.get('page_number')  # 添加
    if numbers:
        number = numbers
        del request.session['page_number']
    else:
        number = request.GET.get("number", 1)
    try:
        page = paginator.page(number)
    except:
        page = paginator.page(1)
    finally:
        msg = request.GET.get("msg")
        if msg:
            return render(request, 'emsapp/emplist.html', {"page": page, "msg": msg})
        return render(request, "emsapp/emplist.html", {"page": page})


# 添加员工
def addEmp(request):
    return render(request, 'emsapp/addEmp.html')


# 添加员工逻辑
def addEmp_logic(request):
    try:
        with transaction.atomic():
            name = request.POST.get('name')
            salary = request.POST.get('salary')
            age = request.POST.get('age')
            # 头像
            head_pic = request.FILES.get('head_pic')
            head_pic.name = str(uuid.uuid4()) + os.path.splitext(head_pic.name)[1]
            emp = Staff.objects.create(name=name, salary=salary, age=age, head_pic=head_pic)
            if emp:
                pagor = Paginator(Staff.objects.all(), per_page=3)
                request.session['page_number'] = pagor.num_pages
                return redirect('emsapp:emplist_logic')
    except Exception as e:
        print(e)


# 删除员工
def delete(request):
    try:
        with transaction.atomic():
            id = request.GET.get('id')
            staff = Staff.objects.get(pk=id)
            staff.delete()
            number = int(request.GET.get('num'))
            pager = Paginator(staff.objects.all(), per_page=3)
            if number > pager.num_pages:
                number -= 1
            request.session['page_number'] = number
            return redirect('emsapp:emplist_logic')
    except Exception as e:
        print(e)
        return JsonResponse({"error": 1, "msg": '删除失败'})


# 更新员工
def updateEmp(request):
    id = request.GET.get('id')
    number = request.GET.get('num')  # 当前的页面
    request.session['page_number'] = number
    try:
        emp = staff = Staff.objects.get(pk=id)
        return render(request, 'emsapp/updateEmp.html', {"emp": emp})
    except:
        return render(request, 'emsapp/updateEmp.html', {"staff": staff})


# 更新员工逻辑
def updareEmp_logic(request):
    try:
        with transaction.atomic():
            id = request.GET.get('id')
            staff = Staff.objects.get(pk=id)
            name = request.POST.get('name')
            salary = request.POST.get('salary')
            age = request.POST.get('age')
            head_pic = request.FILES.get('head_pic')
            ext = os.path.splitext(head_pic.name)[1]
            pic = str(uuid.uuid4()) + ext
            head_pic.name = pic

            staff.name = name
            staff.salary = salary
            staff.age = age
            staff.head_pic = head_pic
            staff.save()
        return redirect('emsapp:emplist_logic')
    except Exception as e:
        print(e)


# 模糊查询
def query(request):
    staff = request.GET.get("s1")
    res = Staff.objects.filter(name__icontains=staff)
    def mydefault(u):
        if isinstance(u, Staff):
            return {'name': u.name, 'salary': u.salary, 'age': u.age}
    return JsonResponse({'staff': list(res)}, safe=False, json_dumps_params={'default': mydefault})
