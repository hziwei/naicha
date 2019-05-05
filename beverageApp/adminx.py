from django.contrib import admin
from .models import *
import xadmin
from xadmin import views
# Register your models here.


# 1.产品列表
class ProduceAdmin(object):
    list_display = ['id', 'product_name', 'product_img', 'product_price', 'product_body', 'product_type', 'product_staple']
    # list_filter=('pro_name',)
    pass


xadmin.site.register(Product, ProduceAdmin)


# 2.产品原料表
class StapleAdmin(object):
    list_display = ['id', 'staple_name', 'staple_price']
    # list_filter=('sta_name',)
    pass


xadmin.site.register(Staple, StapleAdmin)


# 3.产品原料列表
class StockAdmin(object):
    list_display = ['id', 'stock_staple', 'enter_time', 'stock_staple_number']
    # list_filter=('sto_name',)


xadmin.site.register(Stock, StockAdmin)


# 4.促销表
class PromotionAdmin(object):
    list_display = ['id', 'promotion_title', 'promotion_body', 'promotion_img', 'product_rebate']
    # list_filter=('_name',)


xadmin.site.register(Promotion, PromotionAdmin)


# 5.推荐表
class RecommendAdmin(object):
    list_display = ['id', 'recommend_product']
    # list_filter=('stu_name',)


xadmin.site.register(Recommend, RecommendAdmin)


# 6.产品类型
class TypeAdmin(object):
    list_display = ['id', 'type_name', 'product_season_type', 'product_property_type']
    # list_filter=('stu_name',)


xadmin.site.register(Type, TypeAdmin)


# 7.季节表
class Season_typeAdmin(object):
    list_display = ['id', 'season_name']
    # list_filter=('stu_name',)


xadmin.site.register(Season_type, Season_typeAdmin)


# 8.属性表
class Property_typeAdmin(object):
    list_display = ['id', 'property_name']
    # list_filter=('stu_name',)


xadmin.site.register(Property_type, Property_typeAdmin)


# 9.小故事
class ConteAdmin(object):
    list_display = ['id', 'conte_title', 'conte_body']
    # list_filter=('stu_name',)


xadmin.site.register(Conte, ConteAdmin)


# 10.流水详情表
class ReportformsAdmin(object):
    list_display = ['id', 'price', 'time', 'number', 'state']
    # list_filter=('stu_name',)


xadmin.site.register(Reportforms, ReportformsAdmin)


# 11.会员表
class AssociatorTableAdmin:
    list_display = ['id', 'client_name', 'card_number', 'card_password']
    pass


xadmin.site.register(AssociatorTable, AssociatorTableAdmin)


# 12.杯子规格
class CupTableAdmin(object):
    list_display = ['id', 'cup_product', 'cup_size', 'price']
    pass


xadmin.site.register(CupTable, CupTableAdmin)


# 13.店员表
class EmployeeAdmin(object):
    list_display = ['id', 'emp_name', 'emp_password']
    pass


xadmin.site.register(Employee, EmployeeAdmin)


# 店员详情表
class EmployeeDetailAdmin(object):
    list_display = ['id', 'employee', 'name', 'tel', 'addr', 'is_no']
    pass


xadmin.site.register(EmployeeDetail, EmployeeDetailAdmin)

# xadmin 全局数据配置项
class baseSet:
    enable_themes = True  # 启用主题
    use_bootswatch = True  # 切换主题选项
    pass


class GloabSetting(object):
    site_title = '运维管理后台'
    site_head = '运维数据管理中心'
    site_footer = '小故事奶茶'
    menu_style = "accordion"
    pass


xadmin.site.register(views.CommAdminView, GloabSetting)


xadmin.site.register(views.BaseAdminView, baseSet)


# # 会员表
# class Associator_tableAdmin(object):
#     list_display =['id','associatorz_number']
#     # list_filter=('stu_name',)
#
# xadmin.site.register(Associator_table, Associator_tableAdmin)
