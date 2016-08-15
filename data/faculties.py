import json, operator
from salarydb.main.models import Employee, Position, Faculty, Department

f = open("sql/avg_salary_by_faculty.sql")
sql = f.read()

faculties = Faculty.objects.raw(sql)

data = []

for f in faculties:
    data.append(
        {
            'faculty': f.short_name,
            'id': f.id,
            'value': float(f.avg_salary)
        }
    )

response = {
    'values': data,
    'max': data[0]['value']
}

with open('output/faculty_average.json', 'w') as outfile:
    json.dump(response, outfile)

faculties = Faculty.objects.all()

data = []

for f in faculties:
    employees = Employee.objects.filter(faculty=f).order_by("-remuneration")
    if employees:
        e = employees[0]
        data.append(
            {
                'faculty': f.short_name,
                'employee': e.full_name(),
                'url': e.url()['first_name'] + "-" + e.url()['last_name'],
                'value': e.remuneration}
        )

sorted_data = sorted(data, key=lambda k: k['value'])
sorted_data.reverse()

response = {
    'values': sorted_data,
    'max': sorted_data[0]['value']
}


with open('output/faculty_highest.json', 'w') as outfile:
    json.dump(response, outfile)
