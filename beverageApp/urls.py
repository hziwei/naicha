from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    # 1.主页面
    path('', index),
    # 2.产品页面
    path('product/', ProductView.as_view()),
    # 3.促销页面
    path('promotion/', promotion),
    # 4.产品详情页
    url(r'^product/([0-9]+)/$', DetailView.as_view()),
    # 5.小故事页面
    path('story/', storytxt),
    # 6.店员后台页面
    path('employee/', EmployeeView.as_view()),
    # # 7.订单页面
    path('reportforms/', ReportformsView.as_view()),
    # 8.登录页面
    path('login/', LoginIndex.as_view()),
    # 9.登出页面
    path('logout/', logout),
]
