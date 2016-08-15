from main.models import Employee

employees = Employee.objects.all()

for e in employees:
    first = e.first_name.split()
    last  = e.last_name.split()

    first_last = first + last

    e.slug = "-".join(first_last).lower()
    e.save()
    print e.slug
