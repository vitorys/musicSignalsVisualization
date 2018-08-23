# -*- coding: utf-8 -*-

import json
import plotly
import numpy as np

class Graph():
    def __init__(self, matrix):
        self.matrix = matrix

    def processMatrix(self):
        x = []
        y = []

        return (x, y)

    def generateGraph(self):
        print(np.shape(self.matrix))
        graph = dict(
            # Data to plot
            data=[
                # Dots set # 1
                dict(
                    x=[1, 3, 2, 5, 7],
                    y=[2, 6, 4, 2, 3],
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
