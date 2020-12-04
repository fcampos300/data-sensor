import collections
from os import environ
from flask import Flask, Blueprint, request, jsonify, render_template
from matplotlib import pyplot

from repositories.sensor import get_sensors_data, insert_sensor_data
import json
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import matplotlib
matplotlib.use('Agg')


sensor = Blueprint('sensor', __name__)


@sensor.route('/get_sensor', methods=['POST'])
def show():
    content = json.loads(request.data)
    if content is None:
        return jsonify({"message": "JSON not found"})
    else:
        data = json.loads(request.data)
        json_dados = json.dumps(data, ensure_ascii=False, indent=3)
        arq_name = f"{data['timestamp']}_{data['tag'].replace('.', '_')}"

        # Verifica se o campo valor é nulo para definir se o evento é processado ou com erro.
        path = environ.get('PATH_PROCESSED')
        status = 'Processado'
        if not data['valor']:
            path = environ.get('PATH_ERROR')
            status = 'Erro'

        # Gera o arquivo JSON na sua respectiva pasta.
        with open(f"{path}{arq_name}.json", 'w', encoding='utf-8') as arquivo:
            arquivo.write(json_dados)

        # Insere o registro no BD.
        try:
            insert_sensor_data(content, status)
        except Exception as err:
            return jsonify({"message": err})

        return jsonify(content)


@sensor.route(
    '/get_data'
)
def show_data():
    results = get_sensors_data()
    return results


@sensor.route(
    '/view_sensor'
)
def show_sensor_html():
    results = get_sensors_data()
    results = json.loads(results.data)
    sensores_regiao = valida_json(results)

    # Monta o eixo x e y para o gráfico.
    x = list()
    y = list()
    for k in sensores_regiao:
        x.append(k['regiao'])
        y.append(k['total'])

    # Plota o gráfico.
    left = list(range(len(x)))  # Quantidade de colunas deternimada pelo tamanho do eixo x.
    height = y
    tick_label = x
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['red', 'green'])
    plt.ylabel('Eventos')
    plt.xlabel('Regiões')
    plt.title('Eventos por Região')
    plt.savefig('static/images/plot.png')

    return render_template('view.html', resultados=results, regiao=sensores_regiao, url='/static/images/plot.png')


def valida_json(arq):
    validos = list()  # Dados com valores válidos.
    regiao = list()   # Regiões.

    # Retira os valores não numéricos.
    for item in arq:
        try:
            float(item['valor'])
            validos.append(item)
            regiao.append(item['regiao'])
        except ValueError as err:
            pass

    # Lista como as regiões únicas e ordenadas.
    regiao = sorted(set(regiao))

    new_json = list()
    for reg in regiao:
        sensors = list()
        total = 0

        # Separa por região, seta um totalizador para os valores e monta um dicionário com todos os sensores
        # daquela região e seus respectivos valores.
        for it in validos:
            if reg == it['regiao']:
                sensor_dict = {
                    "sensor": it['tag'],
                    "valor": float(it['valor'])
                }
                sensors.append(sensor_dict)
                total += float(it['valor'])

        # Cria uma coleção para contar os valores únicos na lista de sensores.
        contador = collections.Counter()

        # Para cada sensor, some o valor.
        for i in sensors:
            contador[i['sensor']] += i['valor']

        # Cria novamente a lista de sensores e agora adiciona os valores únicos com o vampo valor somado.
        sensors = list()
        for key, value in contador.items():
            sensors.append({"sensor": key, "valor": value})

        # Cria um dicionário com a região, o total e seus sensores.
        dict_reg = {
            "regiao": reg,
            "total": total,
            "sensores": sorted(sensors, key=lambda k: k['sensor'])
        }

        new_json.append(dict_reg)

    return new_json
