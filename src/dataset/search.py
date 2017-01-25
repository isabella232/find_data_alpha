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
    }},
    ignore=400
)


def search_query(query, offset, limit):
    res = es.search(index=settings.ES_INDEX, body={
        "query": {
            "simple_query_string" : {
                "query": "*:{}".format(query),
                "fields": ["summary^5", "_all"],
                "default_operator": "and"
            }
        }
    })

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
