from django.db import models
from django.utils import timezone

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

    class Meta:
        ordering = ["-id"]
        verbose_name = '省份'
        verbose_name_plural = '省份'

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

    class Meta:
        ordering = ["-id"]
        verbose_name = '城市'
        verbose_name_plural = '城市'

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

    class Meta:
        ordering = ["-id"]
        verbose_name = '区域'
        verbose_name_plural = '区域'

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

    class Meta:
        ordering = ["-id"]
        verbose_name = '地址'
        verbose_name_plural = '地址'

