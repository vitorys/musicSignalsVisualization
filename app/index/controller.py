# -*- coding: utf-8 -*-
from app.index.form.params import Params
from flask import Blueprint, render_template, request
import json
import plotly

index_blueprint = Blueprint('index', __name__)


@index_blueprint.route('/', methods=['GET'])
def index():
    form = Params(request.form)
    if (request.method == 'POST' and form.validate()):
        pass

    graph = generateGraphExample()
    return render_template('index.html', graph=graph, form=form)


def generateGraphExample():
    graph = dict(
        # Dados
        data=[
            # Conjunto de dados 1 -> Primeira cor
            dict(
                x=[1, 3, 2, 5, 7],
                y=[2, 6, 4, 2, 3],
                mode='markers'
            ),
            # Conjunto de dados 2 -> Segunda cor cor
            dict(
                x=[1, 2, 3, 4, 5],
                y=[1, 2, 3, 4, 5],
                mode='markers'
            )
        ],
        # Layout
        layout=dict(
            title='Nome do Gráfico'
        )
    )
    graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
