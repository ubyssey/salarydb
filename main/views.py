from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import RequestContext
from django.db.models import Q
import json
from itertools import imap

from .models import Employee, Vote
from .templatetags.main_extras import name_to_url

def get_page_range(page, num_pages, count):

    all_pages = range(num_pages)[1:]

    if page < count:
        return all_pages[:count]

    start = num_pages - count

    if page > start:
        return all_pages[start:]

    start = page - (count/2)
    end = page + (count/2)

    return all_pages[start:end]

def get_next_page(page, num_pages):

    if page == num_pages:
        return False

    return page + 1

def get_prev_page(page):

    if page == 1:
        return False

    return page - 1

def employee(request, first=False, last=False, employee=False):

    if not employee:

        #name_pieces = employee_name.split('-')

        #first_name = ' '.join(name_pieces[:-1])
        #last_name = name_pieces[-1]

        first_name = first
        last_name = last

        employee = Employee.objects.get(first_name__icontains=first_name, last_name__icontains=last_name)

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

    context = {
        'rank': rank,
        'employee': employee,
        'rating': rating,
        'stars': gen_stars(rating, employee.num_ratings),
        'ratings_needed': ratings_needed,
    }

    t = get_template('employee.html')
    c = RequestContext(request, context)
    return HttpResponse(t.render(c))


def gen_stars(rating, num_votes):
    if num_votes < 5:
        return ['empty'] * 5
    stars = []
    for i in range(0,5):
        next = rating - i
        if (next >= 1) or (next >= 0.75):
            stars.append('full')
        elif next >= 0.25:
            stars.append('half')
        else:
            stars.append('empty')
    return stars

def search(request, page=1):

    ITEMS_PER_PAGE = 20

    q = request.GET.get('q', False)

    if page:
        page = int(page)
        if page < 1:
            page = 1
    else:
        page = 1

    start = (page - 1) * ITEMS_PER_PAGE

    filters = {
        'department_id': request.GET.get('dept', False),
        'faculty_id': request.GET.get('fac', False),
        'campus': request.GET.get('campus', False),
        'gender': request.GET.get('gen', False),
    }

    order = request.GET.get('order', 'remuneration')
    dir = str(request.GET.get('dir', 'desc'))

    if dir == "asc":
        dir = ''
    elif dir == "desc":
        dir = '-'

    sort = dir+str(order)

    args = []

    if q:
        words = q.split()
        for word in words:
            args.append(Q(first_name__icontains=word) | Q(last_name__icontains=word))

    for filter in filters:
        value = filters[filter]
        if value:
            kwargs = {
                filter: value,
            }
            args.append(Q(**kwargs))

    results = Employee.objects.filter(*args).order_by(sort)[start:start+ITEMS_PER_PAGE]

    if len(results) == 1:
        return redirect('main.views.employee', name_to_url(results[0]))

    count = Employee.objects.filter(*args).count()

    if count == 0:
        results = False

    num_pages = count / ITEMS_PER_PAGE

    context = {
        'results': results,
        'q': q,
        'count': count,
        'cur_page': page,
        'prev_page': get_prev_page(page),
        'next_page': get_next_page(page, num_pages),
        'pages': num_pages,
        'page_range': get_page_range(page, num_pages, 10),
    }

    t = get_template('search.html')
    c = RequestContext(request, context)
    return HttpResponse(t.render(c))
    #return render_to_response('article.html', context)

def api_search(request):

    q = request.GET.get('q', False)

    args = []
    words = q.split()
    for word in words:
        args.append(Q(first_name__icontains=word) | Q(last_name__icontains=word))

    results = Employee.objects.filter(*args).order_by('last_name')[:10]

    data = []

    for e in results:
        url = e.url()
        data.append({
            'name': e.full_name(),
            'url': url['first_name'] + '-' + url['last_name'],
        })


    return HttpResponse(json.dumps(data), content_type="application/json")

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def quantify(seq, pred=None):
    return sum(imap(pred, seq))


def in_range(i, start, end):
    return i >= start and i <= end

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

    while current < end:
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
