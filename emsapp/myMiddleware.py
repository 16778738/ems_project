# _*_coding:UTF-8 _*_
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin


class MyMiddleware(MiddlewareMixin):  # 自定义的中间件
    def __init__(self, get_response):  # 初始化
        super().__init__(get_response)
        print("中间件已经初始化完毕")

    # view处理请求前执行
    def process_request(self, request):  # 某一个view
        if 'login' not in request.path:
            is_login = request.session.get('login')
            if is_login:
                pass
            elif "regist" in request.path:
                pass
            elif "getCaptcha" in request.path:
                pass
            else:
                return render(request, 'emsapp/login.html')

    # 在process_request之后View之前执行
    def process_view(self, request, view_func, view_args, view_kwargs):
        print("view:", request, view_func, view_args, view_kwargs)

    # view执行之后，响应之前执行
    def process_response(self, request, response):
        print("response:", request, response)
        return response  # 必须返回response

    # 如果View中抛出了异常
    def process_exception(self, request, ex):  # View中出现异常时执行
        print("exception:", request, ex)
