import json

import pydash
import requests

from traffic_aggregator import log

JCYL_URL = "http://servicios.jcyl.es/InviPublica/VIA2DB.json"

PROVINCIAS = {
    "05": "ÁVILA",
    "09": "BURGOS",
    "24": "LEÓN",
    "34": "PALENCIA",
    "37": "SALAMANCA",
    "40": "SEGOVIA",
    "42": "SORIA",
    "47": "VALLADOLID",
    "49": "ZAMORA"
}


@log
def get_events_from_jcyl():
    payload = json.dumps({
        "params": [
            None,
            None,
            None,
            None,
            {}
        ],
        "method": "getIncidenciasActivas",
        "id": 1
    })
    jcyl_response = requests.post(JCYL_URL, data=payload)
    jcyl = pydash.get(jcyl_response.json(), "result", [])
    return convert_list(jcyl)


def convert(item):
    return {
        "provincia": get_provincia(item),
        "icono": "http://servicios.jcyl.es/InviPublica/resources/images/grid/{icono}".format(
            icono=pydash.get(item, "imgCausa")),
        "alias": pydash.get(item, "nomTramo"),
        "descripcion": "{nomTramo} {obsFija}. {obsVariable}. {rutaAlternativa}".format(
            nomTramo=pydash.get(item, "nomTramo"),
            obsFija=pydash.get(item, "obsFija"),
            obsVariable=pydash.get(item, "obsVariable"),
            rutaAlternativa=pydash.get(item, "rutaAlternativa")),
        "suceso": pydash.get(item, "txtTipo"),
        "causa": pydash.get(item, "txtCausa"),
        "carretera": pydash.get(item, "codVial")
    }


def convert_list(items):
    return [convert(item) for item in items]


def get_provincia(item):
    cod_provincia = pydash.get(item, "codProv", "0")
    print(cod_provincia)
    return pydash.get(PROVINCIAS, cod_provincia, "CASTILLA y LEÓN")