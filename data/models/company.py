from django.db import models
from django.utils import timezone
from .place import Province, City, Zone, Address

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

    class Meta:
        ordering = ["-id"]
        verbose_name = '公司性质'
        verbose_name_plural = '公司性质'

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

    class Meta:
        ordering = ["-id"]
        verbose_name = '行业'
        verbose_name_plural = '行业'

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

    @classmethod
    def recent_add_companies(cls):
        return cls.objects.filter(modify_time=cls.objects.latest().modify_time)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "公司"
        verbose_name_plural = "公司"
        ordering = ["-id"]
        get_latest_by = "modify_time"


