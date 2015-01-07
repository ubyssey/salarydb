from django.db.models import Model, CharField, ForeignKey, IntegerField

class Employee(Model):
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    position = ForeignKey('Position', blank=True, null=True)
    faculty = ForeignKey('Faculty', blank=True, null=True)
    department = ForeignKey('Department', blank=True, null=True)
    campus = CharField(max_length=255, choices=[('van', 'Vancouver'), ('oka', 'Okanagan')], blank=True, null=True)
    gender = CharField(max_length=1, choices=[('m', 'Male'), ('f', 'Female')], blank=True, null=True) # 'm' or 'f'
    remuneration = IntegerField()
    expenses = IntegerField()

    rating = IntegerField(default=0)
    num_ratings = IntegerField(default=0)

    class Meta:
        ordering = ['last_name']

    def __str__(self):
        return self.last_name + ', ' + self.first_name

    def get_rating(self):
        if self.num_ratings > 0:
            return float(self.rating) / self.num_ratings
        else:
            return False


class Salary(Model):
    year = IntegerField()
    amount = IntegerField()
    employee = ForeignKey('Employee')

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

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name_plural = "faculties"

class Department(Model):
    name = CharField(max_length=255, blank=True, null=True)
    faculty = ForeignKey('Faculty', blank=True, null=True)
    parent = ForeignKey('Department', blank=True, null=True)
    campus = CharField(max_length=255, choices=[('van', 'Vancouver'), ('oka', 'Okanagan')], blank=True, null=True)
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
