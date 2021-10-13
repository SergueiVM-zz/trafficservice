import json
import time

import pydash
import requests

INFOCAR_URL = "https://infocar.dgt.es/etraffic/BuscarElementos?latNS=44&longNS=5&latSW=27&longSW=-19&zoom=6&accion=getElementos&Camaras=true&SensoresTrafico=true&SensoresMeteorologico=true&Paneles=true&Radares=true&IncidenciasRETENCION=true&IncidenciasOBRAS=false&IncidenciasMETEOROLOGICA=true&IncidenciasPUERTOS=true&IncidenciasOTROS=true&IncidenciasEVENTOS=true&IncidenciasRESTRICCIONES=true&niveles=true&caracter=acontecimiento"
BIZKAIMOVE_URL = "https://www.bizkaimove.com/bm/consulta.json?solicitud=2"


def log(func):
    def wrapper(*args, **kwargs):
        ts = time.time()
        print("Start {functionName}".format(functionName=func.__name__))
        result = func(*args, **kwargs)
        tf = time.time();
        print("Finish {functionName}: Time: {timeInMillis} ms.".format(functionName=func.__name__,
                                                                       timeInMillis=round((tf - ts) * 1000, 1)))

    return wrapper


@log
def get_events_from_infocar():
    infocar_response = requests.get(INFOCAR_URL, verify=False)
    infocar = infocar_response.json()
    return infocar


@log
def get_events_from_bizkaimove():
    bizkaimove_response = requests.get(BIZKAIMOVE_URL, verify=False)
    bizkaimove = bizkaimove_response.text
    bizkaimove = bizkaimove[1:]
    bizkaimove = bizkaimove[:-1]
    bizkaimove = pydash.get(json.loads(bizkaimove), "incidencias.incidencia", [])
    return bizkaimove


@log
def lambda_handler(event, context):
    out = [get_events_from_infocar(), get_events_from_bizkaimove()]
    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET'
        },
        "body": json.dumps(out),
    }


if __name__ == '__main__':
    lambda_handler(None, None)
