import json

import pydash
import requests

from traffic_aggregator import log

BIZKAIMOVE_URL = "https://www.bizkaimove.com/bm/consulta.json?solicitud=2"


@log
def get_events_from_bizkaimove():
    bizkaimove_response = requests.get(BIZKAIMOVE_URL, verify=False)
    bizkaimove = bizkaimove_response.text
    bizkaimove = bizkaimove[1:]
    bizkaimove = bizkaimove[:-1]
    bizkaimove = pydash.get(json.loads(bizkaimove), "incidencias.incidencia", [])
    return convert_list(bizkaimove)


def convert(item):
    return {
        "provincia": "BIZKAIA",
        "icono": None,
        "alias": pydash.get(item, "referencia"),
        "descripcion": "{tipo}: {referencia} {sentido}".format(tipo=pydash.get(item, "tipo"),
                                                               referencia=pydash.get(item, "referencia"),
                                                               sentido=pydash.get(item, "sentido")),
        "suceso": pydash.get(item, "tipo"),
        "causa": pydash.get(item, "tipo"),
        "carretera": pydash.get(item, "carretera")
    }


def convert_list(items):
    return [convert(item) for item in items]
