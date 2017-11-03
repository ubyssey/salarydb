from django.contrib import admin
from salarydb.models import Employee, Salary, Position, Faculty, Department

class SalaryInline(admin.StackedInline):
    model = Salary
    extra = 1

class EmployeeAdmin(admin.ModelAdmin):
    inlines = [SalaryInline,]

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Position)
admin.site.register(Faculty)
admin.site.register(Department)
