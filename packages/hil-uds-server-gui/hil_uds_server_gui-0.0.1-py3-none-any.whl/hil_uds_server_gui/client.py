import requests
from hil.uds.server import Ecu

def get_ecu():
    # url = "http://localhost:8000/ecu"
    url = "http://localhost:8000/ecu"
    response = requests.get(url)
    ecu = Ecu.parse_obj(response.json())
    return ecu

def set_ecu(ecu):
    url = "http://localhost:8000/ecu"
    response = requests.post(url, json=ecu.dict())
    return response