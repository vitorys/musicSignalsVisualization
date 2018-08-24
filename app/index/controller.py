# -*- coding: utf-8 -*-
# Import form
from app.index.form.params import Params

# Import feature extraction algorithms
from app.algorithms.featureExtrators.all import get_gtzan_features
from app.algorithms.featureExtrators.all import get_rp_features
from app.algorithms.featureExtrators.all import get_stft_features
from app.algorithms.grouping.kmeans import getCentroids

from app.algorithms.transformations.pca import reduceDimensionality

# Import graph module
from app.graph.controller import Graph

# Import application requirements
from flask import Blueprint, render_template, request
from werkzeug import secure_filename


index_blueprint = Blueprint('index', __name__)

@index_blueprint.route('/', methods=['GET', 'POST'])
def index():

    form = Params(request.form)

    if (request.method == 'POST' and form.validate()):

        try:
            filename = secure_filename(request.files['musicFile'].filename)
        except:
            print('erro')

        request.files['musicFile'].save('/home/suporte/musicSignalsVisualization/.temp_' + filename)

        # Algorithms here
        extratorAlgorithm = request.form['featureExt']

        if extratorAlgorithm == 'marsyas':
            matrix = get_gtzan_features('.temp_' + filename)
        elif extratorAlgorithm == 'rp':
            matrix = get_rp_features('.temp_' + filename)
        elif extratorAlgorithm == 'stft':
            matrix = get_stft_features('.temp_' + filename)

        matrix = reduceDimensionality(matrix)
        centroids = getCentroids(matrix, 10)

        graph = Graph(matrix, centroids, filename).generateGraph()

        return render_template('index.html', graph=graph , form=form)

    graph = Graph().generateGraph()
    return render_template('index.html', graph=graph , form=form)

