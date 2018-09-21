# -*- coding: utf-8 -*-

import json
import plotly
import numpy as np

class Graph():
    def __init__(self, matrix = None, centroids = None , musicName = ''):
        self.matrix = matrix
        self.centroids = centroids
        self.musicName = musicName

    def processMatrix(self, genericMatrix):
        if(genericMatrix is None):
            return (0, 0)

        xAxis = []
        yAxis = []

        x, y = np.shape(genericMatrix)

        for i in range(0, x):
            xAxis.append(genericMatrix[i][0])
            yAxis.append(genericMatrix[i][1])

        return (xAxis, yAxis)

    def generateGraph(self):
        xAxis, yAxis = self.processMatrix(self.matrix)
        xCentroids, yCentroids = self.processMatrix(self.centroids)
        graph = dict(
            # Data to plot
            data=[
                # Dots set # 1
                dict(
                    x=xAxis,
                    y=yAxis,
                    mode='markers'
                ),
                dict(
                    x=xCentroids,
                    y=yCentroids,
                    mode='markers',
                    name='Centroids',
                )
            ],
            # Layout
            layout=dict(
                title= self.musicName
            )
        )
        graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)

        return graphJSON
