# -*- coding: utf-8 -*-

import json
import plotly
import numpy as np

class Graph():
    def __init__(self, matrix = None, centroids = None , musicName = '', centroid_frame_count=[]):
        self.matrix = matrix
        self.centroids = centroids
        self.musicName = musicName
        self.centroid_frame_count = centroid_frame_count

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

        sizes = map(lambda x: ((x / float(sum(self.centroid_frame_count))) * 30) + 5 , self.centroid_frame_count)

        #print self.centroid_frame_count
        #print sizes

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
                   marker = dict ( size=sizes )
               )
           ],
            # Layout
            layout=dict(
                title= self.musicName
            )
        )
        graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)

        return graphJSON
