import json, operator
from main.models import Employee, Position, Faculty, Department

f = open("sql/avg_salary_by_faculty.sql")
sql = f.read()

faculties = Faculty.objects.raw(sql)

data = []

for f in faculties:
    data.append(
        { 'faculty': f.short_name,
          'value': float(f.avg_salary)}
    )

with open('data/faculty_average.json', 'w') as outfile:
    json.dump(data, outfile)


faculties = Faculty.objects.all()

data = []

for f in faculties:
    e = Employee.objects.filter(faculty=f).order_by("-remuneration")[0]
    data.append(
        { 'faculty': f.short_name,
          'employee': e.full_name(),
          'value': e.remuneration}
    )

sorted_data = sorted(data, key=lambda k: k['value'])
sorted_data.reverse()

with open('data/faculty_higest.json', 'w') as outfile:
    json.dump(sorted_data, outfile)