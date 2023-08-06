from typing import Any, Optional

import requests


def _run_query(query: str) -> Optional[Any]:
    response = requests.get('http://localhost:9090/api/v1/query',
                            params={
                                'query': query
                            }).json()
    try:
        result = response.get('data').get('result')
        return result[0].get('value')[1]
    except Exception:
        return 'N/A'


def throughput():
    return _run_query('rate(ray_num_events_processed[1m])')


def num_replicas():
    return _run_query('ray_num_replicas')


def processor_latency():
    return _run_query('avg_over_time(ray_process_time[1m])')
