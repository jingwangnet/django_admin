from django.db import models
from django.utils import timezone


class Property(models.Model):
    """
    公司性质
    """
    COMPANY_PROPERTY = (
            ('民营', '民营企业'),
            ('合资', '合资企业'),
            ('个体', '个体企业'),
            ('外资', '外资企业')
            )

    name = models.CharField(
            "公司性质名",
            max_length=2,
            choices=COMPANY_PROPERTY,
            default='民营',
            help_text='公司性质'
            )

    def __str__(self):
        return self.name

    def company_count(self):
        return self.company_set.count()

class Industry(models.Model):
    """
    公司的行业
    """
    name = models.CharField(
            '行业',
            max_length=10,
            default='',
            help_text='公司行业',
            )

    info = models.TextField(
            '附加信息',
            blank=True, 
            null=True
            )

    @property
    def company_count(self):
        return self.company_set.count()

    def __str__(self):
        return self.name


## Location info class


class Province(models.Model):
    name = models.CharField(
            '省份',
            max_length=5,
            unique=True,
            help_text='省份'
            )

    @property
    def city_count(self):
        return self.city_set.count()

    @property
    def company_count(self):
        return Company.objects.filter(address__zone__city__province=self).count() 

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(
        '城市',
        max_length=5,
        unique=True,
        help_text='城市'
    )

    province = models.ForeignKey(
        Province, 
        on_delete=models.CASCADE, 
        verbose_name="省份",
        help_text='省份'
    )

    @property
    def zone_count(self,):
        return self.zone_set.count()

    @property
    def company_count(self):
        return Company.objects.filter(address__zone__city=self).count() 

    def __str__(self):
        return self.name


class Zone(models.Model):
    name = models.CharField(
            '区域',
            max_length=10,
            unique=True,
            help_text="区域"
            )

    city = models.ForeignKey(
            City, 
            on_delete=models.CASCADE, 
            help_text="城市",
            verbose_name="城市"
            )


    def company_count(self):
        return Company.objects.filter(address__zone=self).count() 


    def __str__(self):
        return self.name


class Address(models.Model):
    name = models.CharField(
            "地址",
            max_length=10,
            unique=True,
            help_text="区域",
            )

    zone = models.ForeignKey(
            Zone, 
            on_delete=models.CASCADE, 
            verbose_name="区域",
            help_text="区域"
            )


    def company_count(self):
        return self.company_set.count()


    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField('公司',max_length=20, unique=True)
    property =  models.ForeignKey(
            Property,
            on_delete=models.CASCADE,
            help_text="企业性质",
            verbose_name="企业性质",
            blank=True, 
            null=True
            )

    industry  =  models.ManyToManyField(
            Industry,
            help_text="行业",
            verbose_name="行业",
            )

    is_success = models.BooleanField(default=False)
    info = models.TextField(blank=True, null=True)
    create_time = models.DateField('创建日期', auto_now_add=True)
    modify_time = models.DateField('最后修改日期', default=timezone.now)
    address = models.ForeignKey(Address, on_delete=models.CASCADE,blank=True, null=True)


    def get_city(self):
        city = '{city}'.format(city=self.address.zone.city.name)
        return city 
        
    def get_zone(self):
        zone = '{zone}'.format(city=self.address.zone.name)
        return zone 

    def get_address(self):
        address = '{address} {zone}'.format(address=self.address.zone.name,zone=self.address.name)
        return address 
    
    def employees_count(self):
        return self.employees_set.count()

    def __str__(self):
        return self.name


 ### 部门
class Department(models.Model):
    name = models.CharField('部门',max_length=8, unique=True, help_text="部门", blank=True, null=True )

    @property
    def employees_count (self):
        return self.employees_set.count()

    def __str__ (self):
        return self.name


### 职位
class Position(models.Model):
    name = models.CharField('职位',max_length=8, unique=True, help_text="职位")

    def employees_count (self):
        return self.employees_set.count()

    def __str__ (self):
        return self.name

### 职员
class Employees(models.Model):
    # 性别

    GENDER_CHOICES = (
        ('女', '女'),
        ('男', '男'),
    )

    name = models.CharField('姓名', max_length=8)
    gender = models.CharField('性别', max_length=1, choices=GENDER_CHOICES)
    position = models.ForeignKey(
        Position, 
        on_delete=models.CASCADE, 
        help_text="职位",
        verbose_name="职位"
    )
    department = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE, 
        help_text="部门",
        verbose_name="部门"
    )
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        help_text="公司",
        verbose_name="公司"
    )
    phone = models.CharField('手机号码', max_length=11, unique=True, help_text="手机号码")
    tel = models.CharField('电话', max_length=11, unique=True, blank=True, null=True, help_text="电话")
    remark= models.CharField(max_length=20, blank=True, help_text="备注")
    create_time = models.DateField('创建日期', auto_now_add=True)
    modify_time = models.DateField('最后修改日期', default=timezone.now)

    def __str__ (self):
        return self.name

