# -*- coding: utf-8 -*-

import json
import plotly
import numpy as np

class Graph():
    def __init__(self, matrix):
        self.matrix = matrix

    def processMatrix(self):
        xAxis = []
        yAxis = []

        x, y = np.shape(self.matrix)
        print(x)
        for i in range(0, x):
            xAxis.append(self.matrix[i][0])
            yAxis.append(self.matrix[i][1])

        return (xAxis, yAxis)

    def generateGraph(self):
        xAxis, yAxis = self.processMatrix()
        graph = dict(
            # Data to plot
            data=[
                # Dots set # 1
                dict(
                    x=xAxis,
                    y=yAxis,
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
