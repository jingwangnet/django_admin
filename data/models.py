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
            max_length=10,
            default='',
            help_text='公司行业',
            )

    info = models.TextField(
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
            max_length=5,
            unique=True,
            help_text='省份'
            )

    @property
    def city_count(self):
        return self.city_set.count()

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(
            max_length=5,
            unique=True,
            help_text='城市'
            )

    province = models.ForeignKey(
            Province, 
            on_delete=models.CASCADE, 
            help_text='省份'
            )

    @property
    def zone_count(self,):
        return self.zone_set.count()

    def __str__(self):
        return self.name


class Zone(models.Model):
    name = models.CharField(
            max_length=10,
            unique=True,
            help_text="区域"
            )

    city = models.ForeignKey(
            City, 
            on_delete=models.CASCADE, 
            help_text="城市"
            )


    def address_count(self):
        return self.address_set.count()


    def __str__(self):
        return self.name

class Address(models.Model):
    name = models.CharField(
            max_length=10,
            unique=True,
            help_text="地址"
            )

    zone = models.ForeignKey(
            Zone, 
            on_delete=models.CASCADE, 
            help_text="区域"
            )


    def company_count(self):
        company_list = self.company_set.all() 
        return len(company_list)


    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=20, unique=True)
    address = models.ForeignKey(
            Address,
            on_delete=models.CASCADE,
            help_text="地址"
            )

    property =  models.ForeignKey(
            Property,
            on_delete=models.CASCADE,
            help_text="企业性质"
            )

    industry =  models.ManyToManyField(
            Industry,
            help_text="行业"
            )

    is_success = models.BooleanField(default=False)
    info = models.TextField(blank=True, null=True)

    create_time = models.DateField('创建日期', auto_now_add=True)
    modify_time = models.DateField('最后修改日期', default=timezone.now)

    def get_city(self):
        city = '{city}'.format(city=self.zone.city.city_name)
        return city 
        

    def get_address(self):
        address = '{address} {zone}'.format(address=self.zone.zone_name,zone=self.address.address_name)
        return address 
    
    def employees_count(self):
        return self.employees_set.count()

    def __str__(self):
        return self.name


 ### 部门
class Department(models.Model):
    name = models.CharField(max_length=8, unique=True, help_text="部门", blank=True, null=True )

    @property
    def employees_count (self):
        return self.employees_set.count()

    def __str__ (self):
        return self.name


### 职位
class Position(models.Model):
    name = models.CharField(max_length=8, unique=True, help_text="职位")

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
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    phone = models.CharField('手机号码', max_length=11, unique=True)
    tel = models.CharField('电话', max_length=11, unique=True, blank=True, null=True)
    remark= models.CharField('备注', max_length=20, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    create_time = models.DateField('创建日期', auto_now_add=True)
    modify_time = models.DateField('最后修改日期', default=timezone.now)

    def __str__ (self):
        return self.name

