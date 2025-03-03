from search import Search


def count_mood_groups(search: Search):
    query = {"aggs": {"mode_aggregation": {"terms": {"field": "mode"}}}, "size": 0}

    response = search.es.search(index="spotify", body=query)
    print(response["aggregations"]["mode_aggregation"]["buckets"])


def sort_by_energy(search: Search):
    query = {"sort": [{"energy": {"order": "desc"}}]}

    response = search.es.search(index="spotify", body=query)
    print(response["hits"]["hits"])


if __name__ == "__main__":
    es = Search()
    count_mood_groups(es)
    sort_by_energy(es)
