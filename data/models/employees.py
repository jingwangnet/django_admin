from django.db import models
from django.utils import timezone
from .company import Company

### 部门
class Department(models.Model):
    name = models.CharField('部门',max_length=8, unique=True, help_text="部门", blank=True, null=True )

    @property
    def employees_count (self):
        return self.employees_set.count()

    def __str__ (self):
        return self.name

    class Meta:
        ordering = ["-id"]
        verbose_name = '部门'
        verbose_name_plural = '部门'

### 职位
class Position(models.Model):
    name = models.CharField('职位',max_length=8, unique=True, help_text="职位")

    def employees_count (self):
        return self.employees_set.count()

    def __str__ (self):
        return self.name

    class Meta:
        ordering = ["-id"]
        verbose_name = '职位'
        verbose_name_plural = '职位'

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

    @classmethod
    def recent_add_employees(cls):
        return cls.objects.filter(modify_time=cls.objects.latest().modify_time)

    def __str__(self):
        return self.name

    def __str__ (self):
        return self.name

    class Meta:
        ordering = ["-id"]
        get_latest_by = "modify_time"
        verbose_name = '员工'
        verbose_name_plural = '员工'
