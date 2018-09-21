# -*- coding: utf-8 -*-
# Import form
from app.index.form.params import Params
# Import feature extraction algorithms
from app.algorithms.featureExtrators.all import get_gtzan_features, get_rp_features, get_stft_features
from app.algorithms.grouping.kmeans import getCentroids
from app.algorithms.preprocessing.norm import normalize
from app.algorithms.transformations.pca import reduceDimensionality
import numpy as np
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

        extratorAlgorithm, filename, centroids_number, musicPath = getFormData()

        matrix = getFeatureMatrix(extratorAlgorithm, filename)
        matrix_norm = normalize(matrix)

        centroids, distancesCentroid = getCentroids(matrix_norm, centroids_number)
        distancesCentroid = np.array(distancesCentroid)

        centroidClosestPoints = 5
        mais_proximos_todos_centroids = []

        for centroid in xrange(0,centroids_number - 1):
            mais_proximos_centroid = [0] * centroidClosestPoints
            for i, distance in enumerate(distancesCentroid.argsort(axis=0)):
                if distance[centroid] < centroidClosestPoints:
                    mais_proximos_centroid[distance[centroid]] = i

            mais_proximos_todos_centroids.append(mais_proximos_centroid)

        pca = reduceDimensionality(matrix_norm)
        matrix_norm = pca.transform(matrix_norm)
        centroids = pca.transform(centroids)
        graph = Graph(matrix_norm, centroids, filename).generateGraph()
        return render_template('index.html', graph=graph , form=form, musicPath=musicPath)

    graph = Graph().generateGraph()
    return render_template('index.html', graph=graph , form=form)

def getFormData():
    try:
        filename = secure_filename(request.files['musicFile'].filename)
    except:
        print('erro')

    request.files['musicFile'].save('app/.data/' + filename)
    musicPath = '/getMusic/' + filename

    try:
        centroids_number = int(request.form['centroidNumber'])
    except Exception:
        centroids_number = 10

    extratorAlgorithm = request.form['featureExt']
    return extratorAlgorithm, filename, centroids_number, musicPath

def getFeatureMatrix(extratorAlgorithm, filename):
    if extratorAlgorithm == 'marsyas':
        matrix = get_gtzan_features('app/.data/' + filename)
    elif extratorAlgorithm == 'rp':
        matrix = get_rp_features('app/.data/' + filename)
    elif extratorAlgorithm == 'stft':
        matrix = get_stft_features('app/.data/' + filename)
    return matrix

