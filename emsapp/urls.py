# _*_coding:UTF-8 _*_
from django.urls import path
from emsapp import views

app_name = 'emsapp'
urlpatterns = [
    path('login/',views.login, name='login' ),
    path('login1/',views.login1, name='login1' ),
    path('regist/',views.regist, name='regist' ),
    path('addemp/',views.addEmp, name='addEmp' ),
    path('updateemp/',views.updateEmp, name='updateEmp' ),
    path('delete/',views.delete, name='delete' ),
    path('emplist_logic/',views.emplist_logic,name='emplist_logic'),
    path('regist_logic/',views.regist_logic,name='regist_logic'),
    path('addEmp_logic/',views.addEmp_logic,name='addEmp_logic'),
    path('updateEmp_logic/',views.updareEmp_logic,name='updareEmp_logic'),
    path('getCaptcha/',views.getCaptcha,name='getCaptcha'),
    path('query/',views.query,name='query'),

]
