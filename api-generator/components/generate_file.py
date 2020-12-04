from concurrent.futures import ProcessPoolExecutor
import calendar
import os
import random
import requests
import time


def get_region():
    """
    Busca uma região, aleatoriamente, dentro de uma lista.
    :return: Uma região.
    """
    regions = list()
    regions.append('norte')
    regions.append('nordeste')
    regions.append('sudeste')
    regions.append('sul')

    return random.choice(regions)


def get_sensor():
    """
    Busca um número de sensor entre 1 e 5.
    :return: Um sensor.
    """
    return random.randint(1, 6)


def get_value():
    """
    Busca um valor, aleatoriamente, dentro de uma lista.
    :return: Um valor.
    """
    values = list()
    values.append('')
    values.append('')
    values.append('')
    values.append('')
    values.append('')
    values.append('Ok')
    values.append('Ok')
    values.append('Ok')
    values.append('Ok')
    values.append('Ok')
    values.append('Ok')
    values.append('Up')
    values.append('Up')
    values.append('Up')
    values.append('Up')
    values.append('Up')
    values.append('Up')
    values.append('Down')
    values.append('Down')
    values.append('Down')
    values.append('Down')
    values.append('Down')
    values.append('Down')
    values.append(1)
    values.append(2)
    values.append(3)
    values.append(4)
    values.append(5)
    values.append(6)
    values.append(6)
    values.append(7)
    values.append(8)
    values.append(9)
    values.append(10)
    values.append(11)
    values.append(12)
    values.append(13)
    values.append(14)
    values.append(15)

    return random.choice(values)


class SensorFile:

    def __init__(self):
        self._region = get_region()  # Seta uma região aleatória.
        self._sensor = get_sensor()  # Seta um sensor aleatório.
        self._timestamp = calendar.timegm(time.gmtime())
        self._tag = f"brasil.{self._region}.sensor0{self._sensor}"
        self._valor = get_value()

    def get_sensor_data(self):
        return {
            "timestamp": self._timestamp,
            "tag": self._tag,
            "valor": self._valor
        }
