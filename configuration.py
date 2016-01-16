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

EQUATION_DATA = {
    'DISPARITY': {
        'DATA': Equation('Disparity = (Focal * 1/PixelSize) * Base / Distance ', [
            EquationSymbol(name='Disparity', min=0, max=200, value=0, unit='px', isResult=True),
            EquationSymbol(name='Base', min=1, max=200, value=33, unit='cm', factor=1e-2),
            EquationSymbol(name='Focal', min=1, max=100, value=4, unit='mm', factor=1e-3),
            EquationSymbol(name='Distance', min=0, max=200, value=5, unit='m'),
            EquationSymbol(name='PixelSize', min=1, max=20, value=17.7, unit=u'µm', factor=1e-6),
        ])
    },
    'ERROR DISP': {
        'DATA': Equation('Error = Accuracy ', [
            EquationSymbol(name='Accuracy', min=0, max=10, value=1./16, unit='px', isResult=True),
            EquationSymbol(name='Base', min=1, max=200, value=33, unit='cm', factor=1e-2),
            EquationSymbol(name='Focal', min=1, max=100, value=4, unit='mm', factor=1e-3),
            EquationSymbol(name='Distance', min=0, max=200, value=5, unit='m'),
            EquationSymbol(name='PixelSize', min=1, max=20, value=17.7, unit=u'µm', factor=1e-6),
        ])
    },
}

