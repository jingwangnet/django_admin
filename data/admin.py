from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path
from .models import *

admin.site.site_header = "静网数据"
admin.site.site_title = "静网数据 Admin Portal"
admin.site.index_title = "静网数据后台管理"

    
## Property
class PropertyResource(resources.ModelResource):
   
    class Meta:
        model = Property

@admin.register(Property)
class PropertyAdmin(ImportExportModelAdmin):
    list_display = ('name', 'company_count')
    resource_class = PropertyResource


## Industry
class IndustryResource(resources.ModelResource):
   
    class Meta:
        model = Industry

@admin.register(Industry)
class IndustryAdmin(ImportExportModelAdmin):
    list_display = ('name', 'company_count')
    search_fields = ('name',)
   
    resource_class = IndustryResource

## Province
class ProvinceResource(resources.ModelResource):
   
    class Meta:
        model = Province

@admin.register(Province)
class ProvinceAdmin(ImportExportModelAdmin):
    list_display = ('name', 'city_count', 'company_count' )
    resource_class = ProvinceResource
   
## City
class CityResource(resources.ModelResource):
   
    class Meta:
        model = City

@admin.register(City)
class CityAdmin(ImportExportModelAdmin):
    list_display = ('name', 'province', 'zone_count', 'company_count' )
    list_filter = ('province',) 
    resource_class = CityResource
   

## Zone
class ZoneResource(resources.ModelResource):
   
    class Meta:
        model = Zone

@admin.register(Zone)
class ZoneAdmin(ImportExportModelAdmin):
    list_display = ('name', 'city',  'company_count', )
    list_filter = ('city', ) 
    search_fields = ('name',)
    resource_class = ZoneResource
   
## Address
class AddressResource(resources.ModelResource):
   
    class Meta:
        model = Address

@admin.register(Address)
class AddressAdmin(ImportExportModelAdmin):
    list_display = ('name', 'zone',  'company_count', )
    list_filter = ('zone', ) 
    search_fields = ('name',)
    resource_class = AddressResource

class EmployeesInline(admin.StackedInline):
    model = Employees 
    extra = 0 

## Company
class CompanyResource(resources.ModelResource):
   
    class Meta:
        model = Company

@admin.register(Company)
class CompanyAdmin(ImportExportModelAdmin):
    list_display = ('name', 'get_industry', 'is_success', 'property', 'get_address', 'employees_count', 'modify_time' )

    date_hierarchy = 'create_time'
    list_filter = ("property", "industry", 'is_success', )   
    actions = ["mark_success"]
    inlines = [
        EmployeesInline,
    ]

    search_fields = ('name',)
    resource_class = CompanyResource
   
    def mark_success(self, request, queryset):
        queryset.update(is_success=True)

    def get_industry(self, obj):
        return ' '.join([i.name for i in obj.industry.all()])

    
## Department
class DepartmentResource(resources.ModelResource):
   
    class Meta:
        model = Department

@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ('name',  'employees_count')
    resource_class = DepartmentResource
   

## Position
class PositionResource(resources.ModelResource):
   
    class Meta:
        model = Position

@admin.register(Position)
class PositionAdmin(ImportExportModelAdmin):
    list_display = ('name',  'employees_count')
    resource_class = PositionResource
   

## Employees
class EmployeesResource(resources.ModelResource):
   
    class Meta:
        model = Employees

@admin.register(Employees)
class EmployeesAdmin(ImportExportModelAdmin):
    list_display = ('name', 'company',  'department',  'position', 'gender', 'phone', 'tel',  'modify_time', 'create_time')
    list_filter = ('department', 'position' )
   
    
    search_fields = ('name',)
    resource_class = EmployeesResource

