import json

import pydash
import requests

from traffic_aggregator import log

BIZKAIMOVE_URL = "https://www.bizkaimove.com/bm/consulta.json?solicitud=2"


@log
async def get_events_from_bizkaimove():
    try:
        bizkaimove_response = requests.get(BIZKAIMOVE_URL, verify=False)
        bizkaimove = bizkaimove_response.text
        bizkaimove = bizkaimove[1:]
        bizkaimove = bizkaimove[:-1]

        bizkaimove = pydash.get(json.loads(bizkaimove), "incidencias.incidencia", [])
    except Exception as error:
        print("ERROR: Getting info from Bizkaimove" + str(error))
        bizkaimove = []
    return convert_list(bizkaimove)


def convert(item):
    referencia = pydash.get(item, "referencia")
    tipo = pydash.get(item, "tipo")
    referencia = pydash.get(item, "referencia")
    sentido = pydash.get(item, "sentido")
    tipo = pydash.get(item, "tipo")
    carretera = pydash.get(item, "carretera")

    return {
        "provincia": "BIZKAIA",
        "icono": None,
        "alias": f"{carretera} {referencia}",
        "descripcion": f"{tipo}: {referencia} {carretera} {sentido}",
        "suceso": tipo,
        "causa": tipo.upper(),
        "carretera": carretera
    }


def convert_list(items):
    return [convert(item) for item in items if pydash.get(item, "tipo", "").lower() != "obra"]
