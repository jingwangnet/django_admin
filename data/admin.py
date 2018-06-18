import csv
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path
from .models import *

admin.site.site_header = "静网数据"
admin.site.site_title = "静网数据 Admin Portal"
admin.site.index_title = "静网数据后台管理"

## Add export CSV action
class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"
    

@admin.register(Property)
class PrepertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_count')


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_count')
   

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'city_count', )
   

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'zone_count', )
    list_filter = ('province',) 
   


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'city',  'address_count', )
    list_filter = ('city', ) 
   

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('name', 'zone',  'company_count')
    list_filter = ('zone',  )
   

class EmployeesInline(admin.TabularInline):
    model = Employees 
    extra = 1

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ('name', 'get_industry', 'is_success', 'property',  'address', 'employees_count', 'modify_time', 'create_time')

    date_hierarchy = 'create_time'
    list_filter = ("property", "industry", 'is_success',)   
    actions = ["export_as_csv", "mark_success"]
    inlines = [
        EmployeesInline,
    ]

    def mark_success(self, request, queryset):
        queryset.update(is_success=True)

    def get_industry(self, obj):
        return ' '.join([i.name for i in obj.industry.all()])

    

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',  'employees_count')
   

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name',  'employees_count')
   

@admin.register(Employees)
class EmployeesAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ('name', 'company',  'department',  'position', 'gender', 'phone', 'tel',  'modify_time', 'create_time')
    list_filter = ('department', 'position' )
    actions = ["export_as_csv"]
   
    

