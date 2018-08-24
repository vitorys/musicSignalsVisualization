# -*- coding: utf-8 -*-
from wtforms import Form, IntegerField, StringField, TextAreaField, SelectField, validators
from flask_wtf.file import FileField


class Params(Form):

    musicFile = FileField('Música')

    groupAlgorithm = SelectField('Algoritmo de Agrupamento', [
                                 validators.InputRequired()], choices=[('kmeans', 'KMeans')])

    # Kmeans params #
    centroidNumber = IntegerField('Número de Centróides' , [validators.Optional()])

    visualizationAlgorithm = SelectField('Algoritmo de Projeção', [validators.InputRequired()], choices=[('lda', 'Linear Discriminant Analysis'),
                                                                                                         ('pca', 'Principal Component Analysis')])

    featureExt = SelectField('Extrator de Características', choices=[('marsyas', 'Marsyas'),
                                                                ('rp', 'Random Projection'),
                                                                ('stft', 'Short Time Fourier Transform')])
