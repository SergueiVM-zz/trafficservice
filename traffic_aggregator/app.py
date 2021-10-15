import json

from traffic_aggregator import log
from traffic_aggregator.bizkaimove import get_events_from_bizkaimove
from traffic_aggregator.infocar import get_events_from_infocar
from traffic_aggregator.jcyl import get_events_from_jcyl


@log
def lambda_handler(event, context):
    out = [*get_events_from_infocar(), *get_events_from_bizkaimove(), *get_events_from_jcyl()]
    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET'
        },
        "body": json.dumps(out)
    }


if __name__ == '__main__':
    print(lambda_handler(None, None))
