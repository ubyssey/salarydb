import csv

import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

from main.models import Employee, Faculty

employees = Employee.objects.all()

with open('scripts/data/export.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['First Name', 'Last Name', 'Remuneration', 'Expenses', 'Faculty', 'Department', 'Position', 'Gender'])
    for e in employees:
        print e.gender
        writer.writerow([
            e.first_name, 
            e.last_name, 
            e.remuneration, 
            e.expenses, 
            e.faculty.full_name if e.faculty else '', 
            e.department.name if e.department else '', 
            e.position.name if e.position else '', 
            e.gender
            ])