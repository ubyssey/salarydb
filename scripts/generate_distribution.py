import json
from main.models import Employee, Position, Faculty, Department

salaries = Employee.objects.values_list('remuneration', flat=True).order_by('remuneration')

length = len(salaries)

interval = 9000

start = int(round(salaries[0] / interval) * interval)
end = salaries[length-1]

#print employees[length-1].remuneration

current = start

data = []

while (current - interval) < end:
    data.append({
        'x': current,
        'y': Employee.objects.filter(remuneration__range=(current, current+interval)).count()
    })
    current += interval

with open('data/salaries.json', 'w') as outfile:
    json.dump(data, outfile)

with open('data/salaries2.json', 'w') as outfile:
    json.dump(map(int, salaries), outfile)