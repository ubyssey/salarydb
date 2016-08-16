from salarydb.models import Employee, Faculty

employees = Employee.objects.all()
sauder = Faculty.objects.get(short_name='Sauder')
law = Faculty.objects.get(short_name='Law')
pharmacy = Faculty.objects.get(short_name='Pharmacy')
eng_ubco = Faculty.objects.get(id=20)
creative_studies = Faculty.objects.get(id=14)
health = Faculty.objects.get(id=10)

for e in employees:
    if e.department:
        if e.department.faculty:
            e.faculty = e.department.faculty
            e.save()
            print e.faculty
        if e.faculty and e.faculty.id == 18: # Creative Studies
            e.faculty = creative_studies
            e.save()
            print "CREATIVE STUDIES"
        elif e.faculty and e.faculty.id == 17: # Health
            e.faculty = health
            e.save()
            print "HEALTH"
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
        elif e.department.id == 32:
            e.department = None
            e.faculty = eng_ubco
            e.save()
        elif e.department.name == 'Faculty Of Law':
            e.department = None
            e.faculty = law
            e.save()
            print "LAW"
