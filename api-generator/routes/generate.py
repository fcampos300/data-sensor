from concurrent.futures.process import ProcessPoolExecutor

import requests
from flask import Blueprint
from components.generate_file import SensorFile

generate = Blueprint('generate', __name__)


def send():
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/81.0.4044.141 Safari/537.36"}

    sfile = SensorFile()
    json = sfile.get_sensor_data()

    try:
        url = 'http://api-sensor:5000/get_sensor'
        res = session.post(url, json=json, headers=headers)
    except Exception as err:
        print(err)

    return json


@generate.route('/generate/<qtd>')
def show(qtd):
    jsons = list()

    for i in range(int(qtd)):
        executor = ProcessPoolExecutor(max_workers=2)
        task1 = executor.submit(send)

        jsons.append(task1.result())

    return {"arquivos": jsons}
