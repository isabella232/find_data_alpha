from django.db.models import Sum
from django.shortcuts import render
from django.http import JsonResponse

from stats.models import StatRecord

def _apply_date(request, q):
    month = request.GET.get('month')
    year = request.GET.get('year')
    if year:
        q = q.filter(year=year)
    if month:
        q = q.filter(month=month)
    return q

def top(request):
    count = request.GET.get('count') or 10
    stat = request.GET.get('stat')
    orgs = request.GET.get('orgs')

    q = _apply_date(request, StatRecord.objects)
    if stat:
        q = q.filter(statistic=stat)

    if orgs:
        org_list = [o.strip() for o in orgs.split(',')]
        q = q.filter(organisation_id__in=org_list)

    keys = ['dataset_title', 'dataset_id', 'organisation_id', 'statistic']
    if 'year' in request.GET:
        keys.append('year')
    if 'month' in request.GET:
        keys.append('month')

    q = q.values(*keys).annotate(total=Sum('counter'))
    q = q.order_by('-total')

    res = [o for o in q.all()[0:count]]
    return JsonResponse(res, safe=False)


def top_organisation(request, organisation_id):
    count = request.GET.get('count') or 10
    stat = request.GET.get('stat')

    q = _apply_date(request, StatRecord.objects)
    q = q.filter(organisation_id=organisation_id)
    if stat:
        q = q.filter(statistic=stat)

    keys = ['dataset_title', 'dataset_id', 'organisation_id', 'statistic']
    if 'year' in request.GET:
        keys.append('year')
    if 'month' in request.GET:
        keys.append('month')

    q = q.values(*keys).annotate(total=Sum('counter'))
    q = q.order_by('-total')


    res = [o for o in q.all()[0:count]]
    return JsonResponse(res, safe=False)
