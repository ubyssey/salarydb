import json
from main.models import Employee, Position, Faculty, Department

salaries = Employee.objects.values_list('remuneration', flat=True).order_by('remuneration')

length = len(salaries)

interval = 9000

start = int(round(salaries[0] / interval) * interval)
end = salaries[length-1]

current = start

data = {
    'points': [],
    'salaries': map(int, salaries),
}

while (current - interval) < end:
    data['points'].append({
        'x': current,
        'y': Employee.objects.filter(remuneration__range=(current, current+interval)).count()
    })
    current += interval

with open('data/salaries.json', 'w') as outfile:
    json.dump(data, outfile)