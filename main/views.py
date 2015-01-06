from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import RequestContext
from django.db.models import Q
import json


from .models import Employee
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

def employee(request, employee_name, employee=False):

    if not employee:

        name_pieces = employee_name.split('-')

        first_name = ' '.join(name_pieces[:-1])
        last_name = name_pieces[-1]

        employee = Employee.objects.get(first_name__icontains=first_name, last_name__icontains=last_name)

    context = {
        'employee': employee
    }

    t = get_template('employee.html')
    c = RequestContext(request, context)
    return HttpResponse(t.render(c))



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

    if count == 1:
        return

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

    return HttpResponse(json.dumps(map(lambda e: e.first_name + ' ' + e.last_name, results)), content_type="application/json")
