import logging
import urllib

from django.conf import settings

from elasticsearch import Elasticsearch, TransportError

logger = logging.getLogger(__name__)


es = Elasticsearch(settings.ES_HOSTS,
          sniff_on_start=False,
          sniff_on_connection_fail=False,
          sniffer_timeout=None)
es.indices.create(
    index=settings.ES_INDEX,
    body={"mappings" : {
        "datasets" : {
            "properties" : {
                "name" : { "type": "string", "index" : "not_analyzed" },
                "organisation_name" : { "type": "string", "index" : "not_analyzed" }
            }
        }
    },
    "settings" : {
        "index" : {
            "max_result_window" : 75000,
        }
    }},
    ignore=400
)


def search_query(query, filters=None, offset=0, limit=20):

    query_string = None

    if filters:
        filter_string = ' AND '.join('{}:{}'.format(k, v) for k, v in filters.items())
        if query:
            query_string = '{} {}'.format(query, filter_string)
        else:
            query_string = filter_string
    else:
        query_string = query or '*'


    q = {
        "query": {
            "query_string" : {
                "query": query_string,
                "fields": ["summary^2", "title^3", "description^1", "_all"],
                "default_operator": "and"
            }
        },
        "from" : offset, "size" : limit,
    }

    if not query:
        # If no relevance is specified, order by most recently
        # modified first.
        q["sort"] = [
            {"last_edit_date" : {"order" : "desc"}}
        ]

    try:
        res = es.search(index=settings.ES_INDEX, body=q)
    except TransportError as te:
        return [], 0

    datasets = [d['_source'] for d in res['hits']['hits']]

    return datasets, res['hits']['total']


def search_single_dataset(name):
    res = es.search(index=settings.ES_INDEX, body={
        "query": {
            "term" : { "name" : name },
        }
    })

    if res['hits']['total'] != 1:
        return None

    return res['hits']['hits'][0]['_source']

def more_like(dataset):

    # TODO: Remove after re-index
    if not 'organisation_name' in dataset:
        dataset['organisation_name'] = ''

    like = '{title} {summary} {notes} {organisation_name}'.format(**dataset)
    q = {
        "query": {
            "more_like_this" : {
                "fields" : ["title^3", "summary^3", "notes", "organisation_name^2"],
                "like" : like,
                "min_term_freq" : 4,
                "max_query_terms" : 12
            }
        },
        "from" : 0, "size" : 5,
    }

    res = es.search(index=settings.ES_INDEX, body=q)

    if res['hits']['total'] == 0:
        return None

    return [d['_source'] for d in res['hits']['hits']]

