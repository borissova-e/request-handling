from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

from django.conf import settings

import csv
import urllib.parse

def index(request):
    return redirect(reverse(bus_stations))


with open('data-398-2018-08-30.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    CONTENT = []
    for row in reader:
        dict = {'Name': row['Name'], 'Street': row['Street'], 'District': row['District']}
        CONTENT.append(dict)


def bus_stations(request):
    current_page = int(request.GET.get('page', 1))
    paginator = Paginator(CONTENT, settings.ITEMS_PER_PAGE)
    page_obj = paginator.get_page(current_page)

    if page_obj.has_next():
        next = {'page': page_obj.next_page_number()}
        next_page_url = reverse('bus_stations') + '?' + urllib.parse.urlencode(next)
    else:
        next_page_url = None
    if page_obj.has_previous():
        previous = {'page': page_obj.previous_page_number()}
        previous_page_url = reverse('bus_stations') + '?' + urllib.parse.urlencode(previous)
    else:
        previous_page_url = None
    return render(request, 'index.html', context={
        'bus_stations': page_obj,
        'current_page': current_page,
        'prev_page_url': previous_page_url,
        'next_page_url': next_page_url,
    })
