import csv
from main.models import Employee, Position, Faculty, Department

def get_department(raw_name):
    try:
        kwargs = {'raw_name': raw_name}
        return Department.objects.get(**kwargs)
    except Department.DoesNotExist:
        return Department.objects.create(name=raw_name.title(), raw_name=raw_name)

def get_position(raw_name):
    try:
        kwargs = {'raw_name': raw_name}
        return Position.objects.get(**kwargs)
    except Position.DoesNotExist:
        return Position.objects.create(name=raw_name.title(), raw_name=raw_name)

def gen_name(raw_name):
    raw_name = raw_name.decode('latin-1').encode("utf-8")
    pieces = raw_name.split( );
    last_name = pieces[0]
    first_name = ' '.join(pieces[1:])
    return (first_name.title(), last_name.title())

def make_int(value):
    value = value.replace(',', '')
    return int(value)

with open('assets/../assets/salaries.csv', 'U') as salaries:
    reader = csv.reader(salaries)
    for name, position, department, remuneration, expenses in reader:

        first_name, last_name = gen_name(name)
        employee = Employee.objects.create(first_name=first_name, last_name=last_name, remuneration=make_int(remuneration), expenses=make_int(expenses))

        employee.department = get_department(department)
        employee.position = get_position(position)

        employee.save()

        print last_name + ', ' + first_name