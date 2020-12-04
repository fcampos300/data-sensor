from datetime import datetime

import pytz
from flask import jsonify

from database import session
from models.sensor import Sensor


def get_sensors_data():
    """
    Retorna todos os registros da tabela.
    :return: JSON com os dados do modelo.
    """
    lista = []
    for data in session.query(Sensor).all():
        lista.append(data.as_dict())

    return jsonify(lista)


def insert_sensor_data(json, status):
    try:
        insert = Sensor(
            regiao=json['tag'].split('.')[1],
            timestamp=datetime.fromtimestamp(json['timestamp'], pytz.timezone("America/Sao_Paulo")),
            tag=json['tag'],
            valor=json['valor'],
            status=status
        )

        session.add(insert)
        session.commit()
        session.refresh(insert)
    except Exception as err:
        print(err)
        session.rollback()
