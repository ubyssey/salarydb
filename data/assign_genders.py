from salarydb.models import Employee

with open('output/genders.txt', 'U') as file:
    for f in file:
        id, gender = f.split()
        e = Employee.objects.get(id=id)
        e.gender = gender
        e.save()
        print e.full_name() + " -> " + gender
