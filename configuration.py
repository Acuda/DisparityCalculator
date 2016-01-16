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
        'DATA': Equation('x = y**2 + r', [
            EquationSymbol(name='y', min=2, max=10, value=5, unit=''),
            EquationSymbol(name='r', min=2, max=10, value=5, unit=''),
        ])
    },
}

