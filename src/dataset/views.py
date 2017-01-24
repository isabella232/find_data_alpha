import math

from django.http import Http404
from django.shortcuts import render

from .search import search_query, search_single_dataset


def view_dataset(request, slug):
    dataset = search_single_dataset(slug)
    if not dataset:
        raise Http404()

    return render(request, 'dataset/view.html', {'dataset': dataset})


def search(request):
    query = request.GET.get('q')

    page = 1
    try:
        page = int(request.GET.get('page'))
    except:
        page = 1

    datasets, total = search_query(query, offset=(page * 20) - 20, limit=20)
    page_count = math.ceil(float(total) / 20)

    return render(request, 'dataset/search.html', {
        'datasets': datasets,
        'total': total,
        'page_count': page_count,
        'page_range':  range(1, page_count),
        'current_page': page,
        'q': query or ""
    })


