from main.models import Employee
import sexmachine.detector as gender

d = gender.Detector()

employees = Employee.objects.all()

n = 0
for e in employees:
    names = e.first_name.split()
    if len(names) > 0:
        name = names[0]
        g =  d.get_gender(name)
        if g == 'male':
            e.gender = 'm'
            e.save()
            n = n +1
        elif g == 'female':
            e.gender = 'f'
            e.save()
            n = n + 1
        print d.get_gender(e.first_name)

print n