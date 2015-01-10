def get_page_range(page, num_pages, count):

    all_pages = range(num_pages+1)[1:]

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