from django.contrib import admin
from salarydb.models import Employee, Position, Faculty, Department

class PositionInline(admin.StackedInline):
    model = Position
    max_num = 1
    extra = 1

class EmployeeAdmin(admin.ModelAdmin):
    inlines = [PositionInline,]

admin.site.register(Employee)
admin.site.register(Position)
admin.site.register(Faculty)
admin.site.register(Department)
