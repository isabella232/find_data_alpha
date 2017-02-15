from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

from stats.models import StatRecord

def home(request):
    return render(request, "home.html", {})

def download(request, dataset_id, resource_id):
    from dataset.search import es

    try:
        dataset = es.get(index=settings.ES_INDEX, id=dataset_id)['_source']
    except:
        raise Http404()

    url = ''
    for r in dataset['resources']:
        if r['id'] == resource_id:
            url = r['url']
            break

    if not url:
        raise Http404()

    StatRecord.record_now(
        dataset['organisation']['id'],
        dataset['id'],
        dataset['title'],
        'download'
    )

    return HttpResponseRedirect(url)
