# -*- coding: utf-8 -*-
from wtforms import Form, IntegerField, StringField, TextAreaField, SelectField, validators
from flask_wtf.file import FileField


class Params(Form):

    musicFile = FileField('Musica')

    visualizationAlgorithm = SelectField('Algoritmo de Amostragem', [validators.InputRequired()], choices=[('lda', 'Linear Discriminant Analysis'),
                                                                                                           ('pca', 'Principal Component Analysis')])
