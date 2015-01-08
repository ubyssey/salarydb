from main.models import Employee, Faculty

employees = Employee.objects.all()
sauder = Faculty.objects.get(short_name='Sauder')
law = Faculty.objects.get(short_name='Law')

for e in employees:
    if e.department:
        if e.department.faculty:
            e.faculty = e.department.faculty
            e.save()
            print e.faculty
        if e.department.name == 'The Sauder School Of Business':
            e.department = None
            e.faculty = sauder
            e.save()
            print "SAUDER"
        if e.department.name == 'Faculty Of Law':
            e.department = None
            e.faculty = law
            e.save()
            print "LAW"

