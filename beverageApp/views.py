from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from .models import *
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
import random
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, BaseAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework import exceptions
from urllib.request import HTTPPasswordMgrWithPriorAuth
import threading,socket
# Create your views here.
import logging


# base重写
class UserBase(BaseAuthentication):

    def authenticate(self, request):
        # username = request.POST.get('X_USERNAME')
        username = request.POST.get('usertext')
        userpass = request.POST.get('passtext')
        # print(username)
        # print(userpass)
        # username = '张三'
        if not username:
            return None
            pass
        try:
            user = Employee.objects.get(emp_name=username, emp_password=userpass)
            request.session['name'] = username
            request.session['pass'] = userpass
        except user.DoesNotExist:
            # return render(request, 'beverageApp/loginIndex.html')
            raise exceptions.AuthenticationFailed('No such user')
        return (user, None)
        pass
    pass


# 重写permission
class UserPermission(IsAuthenticated):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        # if request.user == '张三':
        if 'name' in request.session and 'pass' in request.session:
            return bool(request.user)
        pass
    pass


# 1.主页面
def index(requests):
    try:
        data = int('你好?')
        print('nihao')
        return render( requests, 'beverageApp/index.html', context={'product': Product.objects.all()[:8]} )
        pass
    except Exception as ex:
        logging.error(ex.args)
        print('nihao')
        col = logging.getLogger('collect')
        col.info(ex.args)
        return render( requests, 'beverageApp/index.html', context={'product': Product.objects.all()[:8]} )
        pass
    return render(requests, 'beverageApp/index.html', context={'product': Product.objects.all()[:8]})
    pass


# 2.产品页面
class ProductView(View):
    '''
    产品的页面的视图
    '''
    def get(self, requests):
        pageNum=requests.GET.get('page')
        print(pageNum)
        if requests.GET.get('type_ID'):
            product = Product.objects.filter(product_type__id=requests.GET.get('type_ID'))
            # data = serializers.serialize('json',product)
            data = productPage(product, pageNum)
            print(data)
            return JsonResponse({'msg': serializers.serialize('json', data[0]), 'page_list': data[1], 'page': data[2]})
            pass
        typeId=Type.objects.all()
        proId = Product.objects.all()
        pro = productPage(proId, pageNum)
        return render(requests,'beverageApp/product.html', context={'proId': pro, 'typeId': typeId})
        pass


# 2.1详细页面
class DetailView(View):
    def get(self, requests, pk):
        product = Product.objects.get(pk=pk)
        # print(product)
        # print(bool(product.product_list.values()))
        if product.product_list.values():
            rebate = product.product_list.all()[0].product_rebate
            pass
        else:
            rebate = 1
            pass
        return render(requests, 'beverageApp/detail.html', context={'product': Product.objects.get(pk=pk), 'rebate':rebate})
        pass

    @csrf_exempt
    def post(self, requests, pk):
        card = requests.POST.get('card')
        # 判断是否有会员卡
        if card:
            try:
                card_obj = AssociatorTable.objects.get(card_number=card)
                if card_obj:
                    if card_obj.card_password == requests.POST.get('pass'):
                        return JsonResponse({'msg': '验证成功...', 'rebate': card_obj.associator_rebate, 'id': card_obj.id})
                    else:
                        return JsonResponse({'msg': '密码错误...'})
                        pass
            except Exception as ex:
                return JsonResponse({'msg': '卡号不存在...'})
                pass
            pass
        try:
            rep = Reportforms()
            product = Product.objects.get(pk=pk)
            rep.proudect = product
            rep.number = requests.POST.get('number')
            rep.employee = Employee.objects.get(emp_name=requests.session['name'])
            rep.price = float(requests.POST.get('price'))*float(requests.POST.get('rebate'))
            rep.save()
            if requests.POST.get('card_id'):
                ass = AssociatorTable.objects.get(id=requests.POST.get('card_id'))
                ass.ass_rep = rep
                ass.save()
        except Exception as ex:
            return JsonResponse({'msg': '店员离岗中...'})
            pass
        # print(requests.POST.get('product'))
        return JsonResponse({'msg': '购买成功...'})
        pass
    pass


# 3.促销页面
def promotion(requests):
    promotion = Promotion.objects.all()
    product = Promotion.objects.all()[0].promotion_product.all()[:8]
    # for i in promotion[0].promotion_product.all():
    #     print(i)
    #     pass
    return render(requests, 'beverageApp/promotion.html', context={'promotion': promotion, 'product': product})
    pass


# 4.小故事页面
def storytxt(requests):
    ass = Conte.objects.all()
    bss = ass[random.randint(0, len(ass)-1)]
    css = bss.conte_body.split('&')
    return render(requests, 'beverageApp/story.html',context={'css': css, 'bss': bss})


# 店员页面
class EmployeeView(APIView):
    authentication_classes = (UserBase, SessionAuthentication)
    permission_classes = (UserPermission, )

    def get(self, requests):
        rep = Reportforms.objects.all()
        rep_state = []
        dict = {}
        if requests.GET.get('id'):
            return JsonResponse({'msg': list(Reportforms.objects.values())})
            pass
        for item in rep:
            if item.employee.emp_name == requests.session['name']:
                if item.state == 1:
                    # print(item.proudect.product_name)
                    dict['id'] = item.id
                    dict['proudect_id'] = item.proudect_id
                    # print(item.proudect.product_name)
                    dict['product'] = item.proudect.product_name
                    dict['price'] = item.price
                    dict['number'] = item.number
                    # 总价格
                    dict['z_price'] = item.price*item.number
                    dict['state'] = item.state
                    # 折扣
                    if item.ass_rep.all():
                        rebate0 = item.ass_rep.all()[0].associator_rebate
                        pass
                    else:
                        rebate0 = 1
                        pass
                    product = item.proudect.product_list.all()
                    if product:
                        rebate = product[0].product_rebate
                        pass
                    else:
                        rebate = 1
                        pass
                    if rebate0 < rebate:
                        rebate = rebate0
                        pass
                    dict['rebate'] = rebate*10
                    rep_state.append(dict)
                    dict = {}
                    pass
                else:
                    pass
                pass
        return render(requests, 'beverageApp/employee.html', context={'rep': rep_state, 'name': requests.session['name']})
        pass

    def post(self, requests):
        if not requests.POST.get('usertext'):
            return JsonResponse({'msg': '登录失败!'})
            pass
        else:
            return JsonResponse({'msg': '登陆成功!'})
            pass
        pass
    pass


# 6.流水详情视图
class ReportformsView(APIView):
    authentication_classes = (UserBase, SessionAuthentication)
    permission_classes = (UserPermission, )

    def get(self, requests):
        rep = Reportforms.objects.all()
        rep_state = []
        dict = {}
        for item in rep:
            if item.employee.emp_name == requests.session['name']:
                if item.state == 0:
                    # print(item.proudect.product_name)
                    dict['id'] = item.id
                    dict['proudect_id'] = item.proudect_id
                    # print(item.proudect.product_name)
                    dict['product'] = item.proudect.product_name
                    dict['price'] = item.price
                    dict['number'] = item.number
                    # 总价格
                    dict['z_price'] = item.price*item.number
                    dict['state'] = item.state
                    # 折扣
                    if item.ass_rep.all():
                        rebate0 = item.ass_rep.all()[0].associator_rebate
                        pass
                    else:
                        rebate0 = 1
                        pass
                    product = item.proudect.product_list.all()
                    if product:
                        rebate = product[0].product_rebate
                        pass
                    else:
                        rebate = 1
                        pass
                    if rebate0 < rebate:
                        rebate = rebate0
                        pass
                    dict['rebate'] = rebate*10
                    rep_state.append(dict)
                    dict = {}
                    pass
                else:
                    pass
                pass
        if requests.GET.get('state'):
            return JsonResponse({'rep': rep_state, 'name': requests.session['name']})
            pass
        return render(requests, 'beverageApp/reportforms.html', context={'rep': rep_state,'name': requests.session['name']})
        pass

    def post(self, requests):

        rep = Reportforms.objects.get(pk=requests.POST.get('id'))
        product = rep.proudect
        for it in list(product.product_staple.all()):
            stock = it.staple.all()
            try:
                s =Stock.objects.get(pk=stock[0].id)
                s.stock_staple_number -= rep.number
                s.save()
                pass
            except Exception as ex:
                return JsonResponse({'msg': '原料库存不足...'})
                pass
            # stock[0].stock_staple_number = 0
            # print(stock[0].stock_staple_number)
            # stock[0].save()
            # print(Stock.objects.values())
            pass
        rep.state = 1
        rep.save()
        return JsonResponse({'msg': '完成订单...'})
        pass
    pass


# 2.2分页
def productPage(pr_list,page):
    '''
    产品页面的分页函数
    :param request:
    :return:
    '''
    # 一页显示6个
    paginator = Paginator(pr_list,6)
    # 总页数
    totalPage = paginator.page_range
    totle = []
    for i in totalPage:
        totle.append(i)
        pass
    # print(totle)
    # 下标
    if not page:
        page = '1'
        pass
    page = int(page)
    list2 = paginator.page(page)
    # try:
    #     pageObj = paginator.page(page)
    #     pass
    # except PageNotAnInteger:
    #     pageObj = paginator.page(1)
    # except EmptyPage:
    #     pageObj =paginator.page(paginator.num_pages)
    return list2, totle, page
    pass


# 登录页面
class LoginIndex(View):

    def get(self, request):
        return render(request, 'beverageApp/loginIndex.html')

    # @csrf_exempt
    # def post(self, requests):
    #     try:
    #         if requests.method == 'POST':
    #             empName = requests.POST.get('usertext')
    #             empPass = requests.POST.get('passtext')
    #             if Employee.objects.all():
    #                 for item in Employee.objects.all():
    #                     if empName == item.emp_name and empPass == item.emp_password:
    #                         return JsonResponse({'msg': '登陆成功!'})
    #                         pass
    #                     else:
    #                         return JsonResponse({'msg': '用户不存在或者密码错误！'})
    #                     pass
    #                 pass
    #             else:
    #                 return JsonResponse({'msg': '用户不存在或者密码错误！'})
    #                 pass
    #     except Exception as ex:
    #         return JsonResponse({'msg': ex.args}, safe=False)
    #     pass
    pass


# 注销页面
def logout(requests):
    del requests.session['name']
    del requests.session['pass']
    return render(requests, 'beverageApp/logged_out.html')
    pass

