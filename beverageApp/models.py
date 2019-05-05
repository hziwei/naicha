from django.db import models
# Create your models here.


# 1.产品列表
class Product(models.Model):
    product_name = models.CharField(max_length=100, verbose_name='产品名')
    product_img = models.ImageField(upload_to='static/img', verbose_name='产品图片')
    product_price = models.FloatField(verbose_name='产品价格')
    product_body = models.TextField(verbose_name='产品信息')
    product_staple = models.ManyToManyField('Staple', verbose_name='产品原料', related_name='product_info')
    product_type = models.ForeignKey('Type', verbose_name='产品类型', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '商品列表'
        verbose_name_plural = verbose_name
        db_table = 'product'
        pass

    def __str__(self):
        return self.product_name
    pass


# 2.产品原料表
class Staple(models.Model):
    staple_name = models.CharField(max_length=150, verbose_name='产品原料')
    staple_price = models.FloatField(verbose_name='原料价格')

    class Meta:
        verbose_name = '产品原料表'
        verbose_name_plural = verbose_name
        db_table = 'staple'
        pass

    def __str__(self):
        return self.staple_name
    pass


# 3.产品原料库存列表
class Stock(models.Model):
    stock_staple = models.ForeignKey('Staple', verbose_name='库存原料', on_delete=models.CASCADE, related_name='staple')
    stock_staple_number = models.IntegerField(verbose_name='库存数量')
    enter_time = models.DateTimeField(auto_now_add=True, verbose_name='入库时间')

    class Meta:
        verbose_name = '产品原料库存列表'
        verbose_name_plural = verbose_name
        db_table = 'stock'
        pass

    def __str__(self):
        return self.stock_staple.staple_name
        pass
    pass


# 4.促销表
class Promotion(models.Model):
    promotion_title = models.CharField(max_length=200, verbose_name='活动标题')
    promotion_body = models.TextField(verbose_name='活动内容')
    promotion_img = models.ImageField(upload_to='static/img', verbose_name='活动图片')
    promotion_product = models.ManyToManyField('Product', verbose_name='促销产品', related_name='product_list')
    # 折扣是放在促销表里 还是产品表里 《待定》
    product_rebate = models.FloatField(default=1.0, verbose_name='产品折扣')

    class Meta:
        verbose_name = '促销表'
        verbose_name_plural = verbose_name
        db_table = 'promotion'
        pass

    def __str__(self):
        return self.promotion_title
    pass


# 5.推荐表
class Recommend(models.Model):
    recommend_product = models.ForeignKey('Product', verbose_name='推荐产品', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '推荐表'
        verbose_name_plural = verbose_name
        db_table = 'recommend'
        pass

    def __str__(self):
        return self.recommend_product.product_name
    pass


# 6.产品类型
class Type(models.Model):
    type_name = models.CharField(max_length=200, verbose_name='类型名')
    product_season_type = models.ForeignKey('Season_type', verbose_name='季节分类', on_delete=models.CASCADE)
    product_property_type = models.ForeignKey('Property_type', verbose_name='产品属性', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '产品类型'
        verbose_name_plural = verbose_name
        db_table = 'type'
        pass

    def __str__(self):
        return self.type_name
    pass


# 7.季节表
class Season_type(models.Model):
    season_name = models.CharField(max_length=200, verbose_name='季节名')

    class Meta:
        verbose_name = '季节表'
        verbose_name_plural = verbose_name
        db_table = 'season_type'
        pass

    def __str__(self):
        return self.season_name
    pass


# 8.属性表
class Property_type(models.Model):
    property_name = models.CharField(max_length=200, verbose_name='属性名')

    class Meta:
        verbose_name = '属性表'
        verbose_name_plural = verbose_name
        db_table = 'property_type'
        pass

    def __str__(self):
        return self.property_name
    pass


# 9.小故事
class Conte(models.Model):
    conte_title = models.CharField(max_length=200, verbose_name='故事标题')
    conte_body = models.TextField(verbose_name='故事内容')

    class Meta:
        verbose_name = '小故事'
        verbose_name_plural = verbose_name
        db_table = 'conte'
        pass

    def __str__(self):
        return self.conte_title
    pass


# 10.流水详情表
class Reportforms(models.Model):
    proudect = models.ForeignKey('Product', verbose_name='产品销售', on_delete=models.CASCADE)
    price = models.FloatField(verbose_name='商品成交价格')
    time = models.DateTimeField(auto_now_add=True, verbose_name='购买商品的时间')
    number = models.IntegerField(verbose_name='购买的数量', default=1)
    state = models.IntegerField(choices=(('否', 0), ('是', 1)), verbose_name='成交状态', default=0)
    employee = models.ForeignKey('Employee', verbose_name='员工', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '流水详情表'
        verbose_name_plural = verbose_name
        db_table = 'reportforms'
        pass


# 11.会员表
class AssociatorTable(models.Model):
    ass_rep = models.ForeignKey('Reportforms', verbose_name='订单信息', on_delete=models.CASCADE, related_name='ass_rep')
    client_name = models.CharField(max_length=100, verbose_name='客户名')
    card_number = models.IntegerField(verbose_name='会员卡号')
    card_password = models.CharField(max_length=100, verbose_name='卡号密码')
    associator_rebate = models.FloatField(default=0.95, verbose_name='产品折扣')

    class Meta:
        db_table = 'Associator_Table'
        verbose_name = '会员表'
        verbose_name_plural = verbose_name
        pass

    def __str__(self):
        return self.client_name
    pass


# 12.杯子规格表
class CupTable(models.Model):
    cup_product = models.ForeignKey('Product', verbose_name='关联产品', on_delete=models.CASCADE, related_name='cup')
    cup_size = models.IntegerField(verbose_name='杯子大小', choices=((1, '大杯'), (2, '中杯'), (3, '小杯')))
    price = models.FloatField(verbose_name='产品价格')

    class Meta:
        db_table = 'Cup_Table'
        verbose_name = '杯子规格表'
        verbose_name_plural = verbose_name
        pass

    pass


# 13.店员表
class Employee(models.Model):
    emp_name = models.CharField(max_length=200, verbose_name='用户名')
    emp_password = models.CharField(max_length=200, verbose_name='用户密码')

    class Meta:
        db_table = 'Employee'
        verbose_name = '店员表'
        verbose_name_plural = verbose_name
        pass

    def __str__(self):
        return self.emp_name
        pass
    pass


# 14.店员详情表
class EmployeeDetail(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, verbose_name='关联店员')
    name = models.CharField(max_length=200, verbose_name='店员名')
    tel = models.CharField(max_length=200, verbose_name='电话号码')
    addr = models.CharField(max_length=200, verbose_name='家庭住址')
    is_no = models.IntegerField(choices=((1, '是'), (2, '否')), verbose_name='是否结婚')

    class Meta:
        db_table = 'Employee_detail'
        verbose_name = '店员详情表'
        verbose_name_plural = verbose_name
        pass

    def __str__(self):
        return self.name
        pass
    pass

