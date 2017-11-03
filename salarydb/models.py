from django.db.models import Model, CharField, ForeignKey, SlugField, IntegerField

CAMPUS_CHOICES = [
    ('van', 'Vancouver'),
    ('oka', 'Okanagan'),
]

GENDER_CHOICES = [
    ('m', 'Male'),
    ('f', 'Female'),
]

class Employee(Model):
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    position = ForeignKey('Position', null=True)
    faculty = ForeignKey('Faculty', null=True)
    department = ForeignKey('Department', null=True)
    campus = CharField(max_length=255, choices=CAMPUS_CHOICES, null=True)
    gender = CharField(max_length=1, choices=GENDER_CHOICES, null=True)

    slug = SlugField(max_length=255)

    rating = IntegerField(default=0)
    num_ratings = IntegerField(default=0)

    class Meta:
        ordering = ['last_name']

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_rating(self):
        if self.num_ratings > 0:
            return float(self.rating) / self.num_ratings
        else:
            return None

    def full_department(self):
        if self.department and self.faculty:
            return '%s - %s' % (self.faculty.full_name, self.department.name)
        elif self.department:
            return self.department.name
        else:
            return self.faculty.full_name

    def url(self):
        first_name = self.first_name.split()

        if len(first_name) > 0:
            first_name = first_name[0]
        else:
            first_name = self.first_name
        return {
            'first_name': first_name.lower(),
            'last_name': self.last_name.lower()
        }

class Salary(Model):
    employee = ForeignKey('Employee')
    year = IntegerField()
    remuneration = IntegerField()
    expenses = IntegerField()

    class Meta:
        verbose_name_plural = 'salaries'

class Position(Model):
    name = CharField(max_length=255, blank=True, null=True)
    raw_name = CharField(max_length=255)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.raw_name

class Faculty(Model):
    full_name = CharField(max_length=255)
    short_name = CharField(max_length=255)
    campus = CharField(max_length=255, choices=CAMPUS_CHOICES, null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name_plural = 'faculties'

class Department(Model):
    name = CharField(max_length=255, blank=True, null=True)
    faculty = ForeignKey('Faculty', null=True)
    parent = ForeignKey('Department', null=True)
    campus = CharField(max_length=255, choices=CAMPUS_CHOICES, null=True)
    raw_name = CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        if self.name:
            if self.parent:
                value = self.parent.name + ' - ' + self.name
            else:
                value = self.name
            if self.campus == 'oka':
                value = value + ' (UBCO)'
            return value
        else:
            return self.raw_name

class Vote(Model):
    ip_address = CharField(max_length=500)
    employee = IntegerField()
    rating = IntegerField()
