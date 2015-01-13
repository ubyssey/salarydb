from main.models import Employee, Faculty

employees = Employee.objects.all()
sauder = Faculty.objects.get(short_name='Sauder')
law = Faculty.objects.get(short_name='Law')
pharmacy = Faculty.objects.get(short_name='Pharmacy')

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
        elif e.department.name == 'Fac.Of Pharmaceutical Sciences':
            e.department = None
            e.faculty = pharmacy
            e.save()
            print "PHARMACY"
        elif e.department.id = 32:
            e.department = None
            e.faculty.id =

        elif e.department.name == 'Faculty Of Law':
            e.department = None
            e.faculty = law
            e.save()
            print "LAW"

