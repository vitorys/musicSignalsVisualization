# -*- coding: utf-8 -*-
# Import form
from app.index.form.params import Params

# Import feature extraction algorithms
from app.algorithms.featureExtrators.all import get_gtzan_features, get_rp_features, get_stft_features
from app.algorithms.grouping.kmeans import getCentroids
from app.algorithms.preprocessing.norm import normalize
from app.algorithms.transformations.pca import reduceDimensionality

import numpy as np

# Audio libraries
import soundfile as sf

# Import graph module
from app.graph.controller import Graph

# Import application requirements
from flask import Blueprint, render_template, request, send_file
from werkzeug import secure_filename


index_blueprint = Blueprint('index', __name__)

@index_blueprint.route('/getMusic/<string:filename>', methods=['GET'])
def getMusic(filename):
    return send_file(".data/" + filename , as_attachment=True)

@index_blueprint.route('/', methods=['GET', 'POST'])
def index():

    form = Params(request.form)

    if (request.method == 'POST' and form.validate()):

        try:
            filename = secure_filename(request.files['musicFile'].filename)
        except:
            print('erro')

        request.files['musicFile'].save('app/.data/' + filename)
        musicPath = '/getMusic/' + filename

        #music = sf.SoundFile('/home/suporte/musicSignalsVisualization/app/.data/' + filename)
        #musicLenght = len(music) / music.samplerate

        centroids_number = int(request.form['centroidNumber'])
        if centroids_number == '':
            centroids_number = 10

        extratorAlgorithm = request.form['featureExt']

        if extratorAlgorithm == 'marsyas':
            matrix = get_gtzan_features('app/.data/' + filename)
        elif extratorAlgorithm == 'rp':
            matrix = get_rp_features('app/.data/' + filename)
        elif extratorAlgorithm == 'stft':
            matrix = get_stft_features('app/.data/' + filename)

        matrix_norm = normalize(matrix)

        centroids, distancesCentroid = getCentroids(matrix_norm, centroids_number)
        distancesCentroid = np.array(distancesCentroid)

        #print [ i if (distance[0] <= 5) for i, distance in enumerate(distancesCentroid.argsort(axis=0))])

        # Distance of point vs all centrids

        centroidClosestPoints = 5
        mais_proximos_todos_centroids = []

        for centroid in xrange(0,centroids_number - 1):

            print("Centroid " + str(centroid))

            mais_proximos_centroid = [0] * centroidClosestPoints

            for i, distance in enumerate(distancesCentroid.argsort(axis=0)):

                if distance[centroid] < centroidClosestPoints:
                    mais_proximos_centroid[distance[centroid]] = i
                    print(distance[centroid], i)
                    print("Inserting "+ str(i) +" into position " + str(distance[centroid]))

            mais_proximos_todos_centroids.append(mais_proximos_centroid)

        print mais_proximos_todos_centroids

        pca = reduceDimensionality(matrix_norm)
        matrix_norm = pca.transform(matrix_norm)
        centroids = pca.transform(centroids)
        graph = Graph(matrix_norm, centroids, filename).generateGraph()

        #featureLenght = float(musicLenght)/len(matrix_norm)

        return render_template('index.html', graph=graph , form=form, musicPath=musicPath)

    graph = Graph().generateGraph()
    return render_template('index.html', graph=graph , form=form)

