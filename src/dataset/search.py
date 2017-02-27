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
                "name" : { "type": "string", "index" : "not_analyzed" }
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


def search_query(query, offset=0, limit=20):
    q = {
        "query": {
            "simple_query_string" : {
                "query": query or '*',
                "fields": ["summary^5", "_all"],
                "default_operator": "and"
            }
        },
        "from" : offset, "size" : limit,
    }

    if query == '*':
        # If no relevance is specified, order by most recently
        # modified first.
        q["sort"] = [
            {"last_edit_date" : {"order" : "desc"}}
        ]

    res = es.search(index=settings.ES_INDEX, body=q)

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

    like = dataset.get('title') + ' ' + dataset.get('notes') + ' ' + dataset.get('summary'),
    q = {
        "query": {
            "more_like_this" : {
                "fields" : ["title", "summary", "notes"],
                "like" : like,
                "min_term_freq" : 3,
                "max_query_terms" : 12
            }
        },
        "from" : 0, "size" : 10,
    }

    res = es.search(index=settings.ES_INDEX, body=q)

    if res['hits']['total'] == 0:
        return None

    return [d['_source'] for d in res['hits']['hits']]

