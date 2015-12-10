from django.shortcuts import redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import RequestContext
from django.db.models import Q
from django.conf import settings

import json
from urllib import urlencode

from helpers import *
from .models import Employee, Vote, Faculty, Department, Position

def landing(request):

    og = {
        'type': 'website',
    }

    context = {
        'title': 'UBC Salary List - The Ubyssey',
        'base_url': settings.BASE_URL,
        'og': og,
    }

    t = get_template('landing.html')
    c = RequestContext(request, context)
    return HttpResponse(t.render(c))

def employee(request, first=False, last=False, employee=False):

    if not employee:
        first_name = first
        last_name = last

        employee = Employee.objects.get(first_name__icontains=first_name, last_name__iexact=last_name)

    rank = {
        'overall': {},
        'faculty': {}
    }

    rank['overall']['salary'] = Employee.objects.all().filter(remuneration__gte=employee.remuneration).order_by('-remuneration').count()
    rank['overall']['expenses'] = Employee.objects.all().filter(expenses__gte=employee.expenses).order_by('-expenses').count()

    if employee.faculty:
        rank['faculty']['salary'] = Employee.objects.all().filter(faculty_id=employee.faculty.id, remuneration__gte=employee.remuneration).order_by('-remuneration').count()
    else:
        rank['faculty'] = False

    rating = employee.get_rating()

    ratings_needed = 5 - employee.num_ratings

    og = {
        'type': 'ubyssey_fb:employee',
    }

    context = {
        'base_url': settings.BASE_URL,
        'title': employee.full_name() + " - UBC Salary List",
        'og': og,
        'rank': rank,
        'employee': employee,
        'rating': rating,
        'stars': gen_stars(rating, employee.num_ratings),
        'ratings_needed': ratings_needed,
    }

    t = get_template('employee.html')
    c = RequestContext(request, context)
    return HttpResponse(t.render(c))


def _filter_filters(model, filters):
    """Returns queryset of `model` objects filtered by `filters`.

    Example: _filter_filters(Position, {'faculty_id':5}) will return all and only the
    Positions existing in the Faculty of Medicine (id=5).
    """
    isactive = lambda q: q != 0

    filters = {k: v for k, v in filters.items()
               if isactive(v)}
    this = model.__name__.lower() + '_id'

    # Filter through reverse foreign keys on Employee.
    return model.objects.filter(**{
        'employee__{}__id'.format(k.split('_')[0]): v
        for k, v in filters.items()
        if k != this
    }).distinct()

    # examples for Position:
    # eg. filters = {'faculty_id': 5}
    # >> Position.objects.filter(employee__faculty__id=5)
    # eg. filters = {'faculty_id': 5, 'department_id': 16, 'position_id': 2}
    # >> Position.objects.filter(employee__faculty__id=5,
    #                            employee__department__id=16)


def search(request):

    ITEMS_PER_PAGE = 20

    page = int(request.GET.get('pg', 1))

    if page < 1:
        page = 1

    start = (page - 1) * ITEMS_PER_PAGE


    q = request.GET.get('q', False)

    params = {}
    args = []

    if q:
        params['q'] = q
        words = q.split()
        for word in words:
            args.append(Q(first_name__icontains=word) | Q(last_name__icontains=word))

    fields = ['department_id', 'faculty_id', 'position_id']
    filters = {}

    for field in fields:
        val = request.GET.get(field, False)
        if val:
            args.append(Q(**{field: val}))
            params[field] = filters[field] = val
        else:
            filters[field] = 0

    query_string = '?' + urlencode(params)

    if query_string:
        query_symbol = '&'
    else:
        query_symbol = '?'

    order = request.GET.get('order', 'remuneration')
    dir = str(request.GET.get('dir', 'desc'))

    if dir == "asc":
        dir = ''
    elif dir == "desc":
        dir = '-'

    sort = dir+str(order)

    results = Employee.objects.filter(*args).order_by(sort)[start:start+ITEMS_PER_PAGE]

    if len(results) == 1:
        e = results[0]
        return redirect('main.views.employee', e.url()['first_name'], e.url()['last_name'])

    count = Employee.objects.filter(*args).count()

    if count == 0:
        results = False

    num_pages = count / ITEMS_PER_PAGE

    context = {
        'title': "Search results - UBC Salary List",
        'query_symbol': query_symbol,
        'query_string': query_string,
        'base_url': settings.BASE_URL,
        'results': results,
        'q': q,
        'count': count,
        'cur_page': page,
        'prev_page': get_prev_page(page),
        'next_page': get_next_page(page, num_pages),
        'pages': num_pages,
        'page_range': get_page_range(page, num_pages, 10),
        'filters': filters,
        'filter_faculties': _filter_filters(Faculty, filters),
        'filter_departments': _filter_filters(Department, filters),
        'filter_positions': _filter_filters(Position, filters),
    }

    t = get_template('search.html')
    c = RequestContext(request, context)
    return HttpResponse(t.render(c))

def api_search(request):

    q = request.GET.get('q', '')

    args = [Q(first_name__icontains=word) | Q(last_name__icontains=word)
            for word in q.split()]

    results = Employee.objects.filter(*args).order_by('last_name')[:10]

    data = []

    for e in results:
        url = e.url()
        data.append({
            'name': e.full_name(),
            'url': url['first_name'] + '-' + url['last_name'],
        })


    return HttpResponse(json.dumps(data), content_type="application/json")

def api_faculty(request, id):

    interval = 10000

    employees = Employee.objects.filter(faculty_id=id).values_list('remuneration', flat=True).order_by('remuneration')
    start = int(round(employees[0] / interval) * interval)
    end = employees[len(employees)-1]

    current = start

    data = {
        'points': [],
        'salaries': map(int, employees),
    }

    while (current - interval) < end:
        data['points'].append({
            'x': current,
            'y': quantify(employees, lambda i: in_range(i, current, current+interval))
        })
        current += interval

    return HttpResponse(json.dumps(data), content_type="application/json")

def api_department(request, id):

    interval = 10000

    employees = Employee.objects.filter(department_id=id).values_list('remuneration', flat=True).order_by('remuneration')
    start = int(round(employees[0] / interval) * interval)
    end = employees[len(employees)-1]

    current = start

    data = {
        'points': [],
        'salaries': map(int, employees),
    }

    while (current - interval) < end:
        data['points'].append({
            'x': current,
            'y': quantify(employees, lambda i: in_range(i, current, current+interval))
        })
        current += interval

    return HttpResponse(json.dumps(data), content_type="application/json")

def api_vote(request, id):

    ip = get_client_ip(request)

    response = {
        'success': False,
        'ip': ip
    }

    votes = Vote.objects.filter(ip_address=ip, employee=id).count()

    if votes > 0:
        return HttpResponse(json.dumps(response), content_type="application/json")

    rating = request.GET.get('rating', False)

    if rating:
        rating = int(rating)
        if rating >= 1 and rating <= 5:
            employee = Employee.objects.get(id=id)
            employee.rating = int(employee.rating) + rating
            employee.num_ratings = int(employee.num_ratings) + 1
            employee.save()

            vote = Vote.objects.create(ip_address=ip, employee=id, rating=rating)
            vote.save()

            response['success'] = True

    return HttpResponse(json.dumps(response), content_type="application/json")
