# -*- coding: utf-8 -*-
# Import form
from app.index.form.params import Params
# Import feature extraction algorithms
from app.algorithms.featureExtrators.all import get_gtzan_features, get_rp_features, get_stft_features
from app.algorithms.grouping.kmeans import getCentroids
from app.algorithms.preprocessing.norm import normalize
from app.algorithms.transformations.pca import reduceDimensionality
# Import utils tools
import numpy as np
# Import graph module
from app.graph.controller import Graph
# Import application requirements
from flask import Blueprint, render_template, request, send_file
from werkzeug import secure_filename

from librosa.core import frames_to_time

index_blueprint = Blueprint('index', __name__)

@index_blueprint.route('/getMusic/<string:filename>', methods=['GET'])
def getMusic(filename):
    return send_file(".data/" + filename , as_attachment=True)

@index_blueprint.route('/', methods=['GET', 'POST'])
def index():

    form = Params(request.form)

    # if user submit the form
    if (request.method == 'POST' and form.validate()):
        # Get data from form
        extratorAlgorithm, filename, centroids_number, musicPath = getFormData()

        # Extract features, then normalize
        matrix = getFeatureMatrix(extratorAlgorithm, filename)
        matrix_norm = normalize(matrix)

        # Get the centroids and calculate the distance to all frames
        centroids, distancesCentroid = getCentroids(matrix_norm, centroids_number)
        distancesCentroid = np.array(distancesCentroid)

        # Define the number of closest frames from centroids to get
        centroidClosestPoints = 5

        # Get the ID of frames closest to each centroid
        closest_frames_idx = distancesCentroid.argsort(axis=0).T[:,:5].tolist()
        centroid_frame_counts= np.bincount(np.argmin(distancesCentroid, axis=1))

        # Get the time from each frame
        tempos = frames_to_time(closest_frames_idx, sr=44100, hop_length=1024, n_fft=2048)
        tempos = tempos.tolist()

        # Apply some transformations
        pca = reduceDimensionality(matrix_norm)
        matrix_norm = pca.transform(matrix_norm)
        centroids = pca.transform(centroids)

        # Generate and encode graph to send to view
        graph = Graph(matrix_norm, centroids, filename, centroid_frame_count=centroid_frame_counts).generateGraph()

        # Send all structures to the view
        return render_template('index.html', graph=graph , form=form, musicPath=musicPath, tempos=tempos)

    # Generate an empty graphic
    graph = Graph().generateGraph()
    return render_template('index.html', graph=graph , form=form)

def getFormData():
    # Get data from form
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
    # Select the feature extractor and return the matrix of features
    if extratorAlgorithm == 'marsyas':
        matrix = get_gtzan_features('app/.data/' + filename)
    elif extratorAlgorithm == 'rp':
        matrix = get_rp_features('app/.data/' + filename)
    elif extratorAlgorithm == 'stft':
        matrix = get_stft_features('app/.data/' + filename)
    return matrix

