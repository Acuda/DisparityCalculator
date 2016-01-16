#!/usr/bin/env python2
#-*- coding: utf-8 -*-
#
#Author: Björn Eistel
#Contact: <eistel@gmail.com>
#
# THIS SOURCE-CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED. IN NO  EVENT WILL THE AUTHOR BE HELD LIABLE FOR ANY DAMAGES ARISING FROM
# THE USE OF THIS SOURCE-CODE. USE AT YOUR OWN RISK.

from Equation import *

EQUATION_ORDER = [
    'Pixel-Size',
    'DISPARITY',
    'ERROR DISPARITY',
]

EQUATION_DATA = {
    'Pixel-Size': {
        'DATA': Equation('PixelSize = SensorLength / NumPixel ', [
            EquationSymbol(name='PixelSize', min=1, max=20, value=17, unit=u'µm', factor=1e-6, isResult=True),
            EquationSymbol(name='SensorLength', min=1, max=50, value=17.408, unit='mm', factor=1e-3),
            EquationSymbol(name='NumPixel', min=600, max=2048, value=1024, unit='px'),
        ])
    },
    'DISPARITY': {
        'DATA': Equation('Disparity = (Focal * 1/PixelSize) * Base / Distance', [
            EquationSymbol(name='Disparity', min=0, max=160, value=64, unit='px', isResult=True),
            EquationSymbol(name='Base', min=1, max=200, value=43.520, unit='cm', factor=1e-2),
            EquationSymbol(name='Focal', min=1, max=30, value=15, unit='mm', factor=1e-3),
            EquationSymbol(name='Distance', min=6, max=100, value=6, unit='m'),
            EquationSymbol(name='PixelSize', min=1, max=20, value=17, unit=u'µm', factor=1e-6, extern='Pixel-Size'),
        ])
    },
    'ERROR DISPARITY': {
        'DATA': Equation('DistanceError = (Focal * 1/PixelSize) * Base / Disparity - (Focal * 1/PixelSize) * Base / (Disparity + AccuracyFactor*1./16)', [
            EquationSymbol(name='DistanceError', min=0, max=100, value=5, unit='m', factor=1, isResult=True),
            EquationSymbol(name='AccuracyFactor', min=1, max=10, value=5),
            EquationSymbol(name='Disparity', min=0, max=160, value=0, unit='px', extern='DISPARITY'),
            EquationSymbol(name='Base', min=1, max=200, value=33, unit='cm', factor=1e-2, extern='DISPARITY'),
            EquationSymbol(name='Focal', min=1, max=100, value=4, unit='mm', factor=1e-3, extern='DISPARITY'),
            EquationSymbol(name='PixelSize', min=1, max=20, value=17.7, unit=u'µm', factor=1e-6, extern='DISPARITY'),
        ])
    },
}

