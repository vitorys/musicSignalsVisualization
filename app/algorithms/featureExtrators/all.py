# -*- coding: utf-8 -*-
# TODO: Separete features extractors into different files
import librosa
import numpy as np
import scipy
from six import integer_types

def to_texture(data, texture_size, mean=True, variance=True):

    w = texture_size
    N = len(data)

    ret = np.array(())
    ret.shape = (0,0)
    dT = data.T
    it = 1 if dT.ndim ==  1 else dT.shape[0]

    #print 'N:', N

    n = 0
    S = np.array([0.0] * it)
    m = np.array([0.0] * it)

    #print dT.shape

    saida = np.zeros((data.shape[0], data.shape[1]*2))

    #print 'saida', saida.shape

    for x in dT[:,:w].T:
        n+=1
        n_m = m + (x-m)/n
        n_s = S + (x-m)*(x-n_m)
        m = n_m
        S = n_s

    y = np.concatenate((m, S/n), axis=0)
    saida[n] = y
    #print y, y.shape, n

    for i in xrange(w, N):
        m = n_m
        n_m = m + (dT[:,i]-m)/n - (dT[:,i-w]-m)/n
        S = S + ( (dT[:,i] - n_m) * (dT[:,i] - m) ) - ( ( dT[:,i-w] - m )*( dT[:,i-w] - n_m ) )

        y = np.concatenate((m, S/n), axis=0)
        saida[i] = y

    #print saida[n]

    if mean and variance:
        return saida[w:,:]

    if mean:
        return saida[w:,:saida.shape[1]/2]

    if variance:
        return saida[w:,saida.shape[1]/2:]

    return None

def flatness(A):
    """Spectral flatness of each frame"""
    return np.exp(  np.mean(np.log(np.maximum(A, 0.0001)), 0) ) / \
       (np.mean(A, 0) + (10**(-6)))

def flux(A):
    """Spectral flux of each frame"""
    a = np.diff(A, axis = 1)
    s = np.sum(np.maximum(a, 0), axis=0)
    s0 = np.sum(A, axis=0) + (10**(-6))
    return np.hstack ((np.array([0]), s))/np.maximum(s0, 0.0000001)

def energy(A):
    """Energy of each frame"""
    return np.sum(A**2 , 0)

def get_gtzan_features(input_file, params=dict()):
    #Parametros deste extrator!
    n_mfcc = params['n_mfcc'] if params.has_key('n_mfcc') else 20
    n_fft = params['n_fft'] if params.has_key('n_fft') else 2048
    hop_length = params['hop_length'] if params.has_key('hop_length') else 1024
    target_sr = params['target_sr'] if params.has_key('target_sr') else 44100
    deltas = params['deltas'] if params.has_key('deltas') else True
    delta_deltas = params['delta_deltas'] if params.has_key('delta_deltas') else True
    texture_window_size = params['texture_window_size'] if params.has_key('texture_window_size') else 200

    y, sr = librosa.load(input_file, sr=target_sr, mono=True)

    #centering data around mean zero, std_dev 1
    m = np.mean(y)
    v = np.var(y)
    y = (y-m) / np.sqrt(v)

    w = scipy.signal.hamming(n_fft, sym=False)

    stft = np.abs(librosa.core.stft(y, n_fft=n_fft, hop_length=hop_length, window=w, win_length=n_fft, center=True))

    mfccs = librosa.feature.mfcc(y, sr=sr, n_mfcc=n_mfcc, n_fft=n_fft, hop_length=hop_length)

    en = energy(stft)
    scentroid = librosa.feature.spectral_centroid(S=stft, sr=sr, n_fft=n_fft, hop_length=hop_length, freq=None)
    srolloff = librosa.feature.spectral_rolloff(S=stft, sr=sr, n_fft=n_fft, hop_length=hop_length, freq=None )
    flat = flatness(stft)
    flx = flux(stft)

    zcr = librosa.feature.zero_crossing_rate(y, frame_length=n_fft, hop_length=hop_length)

    feats = np.vstack((mfccs, scentroid, srolloff, flat, flx , en, zcr))

    if deltas:
        d = librosa.feature.delta(feats, order=1)
    else:
        d = np.empty((0,feats.shape[1]))

    if delta_deltas:
        dd = librosa.feature.delta(feats, order=2)
    else:
        dd = np.empty((0,feats.shape[1]))

    feats = np.vstack((feats, d, dd))

    if texture_window_size is not None:
        feats = to_texture(feats.T, texture_window_size)

    return feats

def get_gaussian_random_matrix(mean, stdev, shape, random_state=None, out_file=None):

    if random_state is None:
        random_state = np.random

    if isinstance(random_state, integer_types):
        random_state = np.random.RandomState(random_state)

    m = random_state.normal(mean, stdev, size=shape)

    if out_file is not None:
        dill.dump(m, open(out_file, 'w'))

    return m

def get_rp_features(input_file, params=dict()):

    #Parametros deste extrator!
    sr = params['target_sr'] if params.has_key('target_sr') else 44100
    n_fft = params['n_fft'] if params.has_key('n_fft') else 2048
    hop_length = params['hop_length'] if params.has_key('hop_length') else 1024
    projection_matrix = params['projection_matrix'] if params.has_key('projection_matrix') else None
    mel_bins = params['mel_bins'] if params.has_key('mel_bins') else 128
    in_db = params['in_db'] if params.has_key('in_db') else True
    random_seed = params['random_seed'] if params.has_key('random_seed') else 1
    target_dimensionality = params['target_dimensionality'] if params.has_key('target_dimensionality') else 50
    deltas = params['deltas'] if params.has_key('deltas') else True
    delta_deltas = params['delta_deltas'] if params.has_key('delta_deltas') else True
    texture_window_size = params['texture_window_size'] if params.has_key('texture_window_size') else 200

    y, sr = librosa.load(input_file, sr=sr, mono=True)

    m = np.mean(y)
    v = np.var(y)
    y = (y-m) / np.sqrt(v)

    w = scipy.signal.hamming(n_fft, sym=False)

    spectrum = np.abs(librosa.core.stft(y, n_fft=n_fft, hop_length=hop_length, window=w, win_length=n_fft, center=True))

    if mel_bins is not None:
        spectrum = librosa.feature.melspectrogram(S=spectrum, sr=sr, n_fft=n_fft, hop_length=hop_length, power=2.0, n_mels=mel_bins)

    if in_db:
        spectrum = librosa.power_to_db(spectrum)

    if projection_matrix is None:
        source_dim = mel_bins if mel_bins is not None else n_fft
        projection_matrix = get_gaussian_random_matrix(0.0, 1.0,
            (source_dim,target_dimensionality), random_state=random_seed)

    feats = spectrum.T.dot(projection_matrix)

    if deltas:
        pad = np.zeros((1, feats.shape[1]))
        d = np.vstack((pad, np.diff(feats, axis=0)))
        if delta_deltas:
            pad = np.zeros((1, d.shape[1]))
            dd = np.vstack((pad, np.diff(d, axis=0)))
            feats = np.hstack((feats, d, dd))
        else:
            feats = np.hstack((feats, d))

    if texture_window_size is not None:
        feats = to_texture(feats, texture_window_size)

    return feats

def get_stft_features(input_file, params=dict()):

    #Parametros deste extrator!
    sr = params['target_sr'] if params.has_key('target_sr') else 44100
    n_fft = params['n_fft'] if params.has_key('n_fft') else 2048
    hop_length = params['hop_length'] if params.has_key('hop_length') else 1024
    mel_bins = params['mel_bins'] if params.has_key('mel_bins') else 128
    in_db = params['in_db'] if params.has_key('in_db') else True
    deltas = params['deltas'] if params.has_key('deltas') else True
    delta_deltas = params['delta_deltas'] if params.has_key('delta_deltas') else True
    texture_window_size = params['texture_window_size'] if params.has_key('texture_window_size') else 200

    y, sr = librosa.load(input_file, sr=sr, mono=True)

    m = np.mean(y)
    v = np.var(y)
    y = (y-m) / np.sqrt(v)

    w = scipy.signal.hamming(n_fft, sym=False)

    spectrum = np.abs(librosa.core.stft(y, n_fft=n_fft, hop_length=hop_length, window=w, win_length=n_fft, center=True))

    if mel_bins is not None:
        spectrum = librosa.feature.melspectrogram(S=spectrum, sr=sr, n_fft=n_fft, hop_length=hop_length, power=2.0, n_mels=mel_bins)

    if in_db:
        spectrum = librosa.power_to_db(spectrum)

    feats = spectrum.T

    if deltas:
        pad = np.zeros((1, feats.shape[1]))
        d = np.vstack((pad, np.diff(feats, axis=0)))
        if delta_deltas:
            pad = np.zeros((1, d.shape[1]))
            dd = np.vstack((pad, np.diff(d, axis=0)))
            feats = np.hstack((feats, d, dd))
        else:
            feats = np.hstack((feats, d))

    if texture_window_size is not None:
        feats = to_texture(feats, texture_window_size)

    return feats

if __name__ == "__main__" :
    audio_file = librosa.util.example_audio_file()

    gtzan_feats = get_gtzan_features(audio_file)
    print gtzan_feats.shape

    random_feats = get_rp_features(audio_file)
    print random_feats.shape

    stft_feats = get_stft_features(audio_file)
    print stft_feats.shape
