import pydash
import requests

from traffic_aggregator import log

INFOCAR_URL = "https://infocar.dgt.es/etraffic/BuscarElementos?latNS=44&longNS=5&latSW=27&longSW=-19&zoom=6&accion=getElementos&Camaras=true&SensoresTrafico=true&SensoresMeteorologico=true&Paneles=true&Radares=true&IncidenciasRETENCION=true&IncidenciasOBRAS=false&IncidenciasMETEOROLOGICA=true&IncidenciasPUERTOS=true&IncidenciasOTROS=true&IncidenciasEVENTOS=true&IncidenciasRESTRICCIONES=true&niveles=true&caracter=acontecimiento"


@log
async def get_events_from_infocar():
    try:
        infocar_response = requests.get(INFOCAR_URL, verify=False)
        infocar = infocar_response.json()
    except Exception as error:
        print("ERROR: Getting info from Inforcar" + str(error))
        inforcar = []

    return convert_list(infocar)


def convert(item):
    return {
        "provincia": pydash.get(item, "provincia"),
        "icono": "https://infocar.dgt.es/etraffic/img/iconosIncitar/{icono}".format(icono=pydash.get(item, "icono")),
        "alias": pydash.get(item, "alias"),
        "descripcion": pydash.get(item, "descripcion"),
        "suceso": pydash.get(item, "suceso"),
        "causa": pydash.get(item, "causa"),
        "carretera": pydash.get(item, "carretera")
    }


def convert_list(items):
    return [convert(item) for item in items]
