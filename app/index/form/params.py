# -*- coding: utf-8 -*-
from wtforms import Form, IntegerField, StringField, TextAreaField, SelectField, validators
from flask_wtf.file import FileField


class Params(Form):

    musicFile = FileField('Music File')

    groupAlgorithm = SelectField('Grouping Algorithm', [
                                 validators.InputRequired()], choices=[('kmeans', 'KMeans')])

    # Kmeans params #
    centroidNumber = IntegerField('Centroids Number' , [validators.Optional()])

#choices=[('lda', 'Linear Discriminant Analysis'),
#    ('pca', 'Principal Component Analysis')]

    visualizationAlgorithm = SelectField('Projection Algorithm', [validators.InputRequired()], choices=[('pca', 'Principal Component Analysis')])

    featureExt = SelectField('Feature Extractor', choices=[('marsyas', 'Marsyas'),
                                                                ('rp', 'Random Projection'),
                                                                ('stft', 'Short Time Fourier Transform')])
