#!/usr/bin/env python2
#-*- coding: utf-8 -*-
#
#Author: Björn Eistel
#Contact: <eistel@gmail.com>
#
# THIS SOURCE-CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED. IN NO  EVENT WILL THE AUTHOR BE HELD LIABLE FOR ANY DAMAGES ARISING FROM
# THE USE OF THIS SOURCE-CODE. USE AT YOUR OWN RISK.

import sympy
from sympy.core.symbol import Symbol


class EquationSymbol(object):
    def __init__(self, name, min=0, max=1000, value=500, unit=''):
        self.name = name
        self.symbol = sympy.symbols(name)
        self.min = min
        self.max = max
        self.value = value
        self.unit = unit

    def __repr__(self):
        return '#EquationSymbol %s, %d %d %d#' % (self.name, self.min, self.value, self.max)


class Equation(object):
    def __init__(self, expression, equation_symbol_list=[]):
        self.expression = expression

        expression_left_hand, expression_right_hand = expression.split('=')
        sympy_expression_left_hand = sympy.sympify(expression_left_hand)
        sympy_expression_right_hand = sympy.sympify(expression_right_hand)
        self.sympy_equation = sympy.Eq(sympy_expression_left_hand, sympy_expression_right_hand)

        self.symbols = list(set(self.findSymbols(self.sympy_equation)))

        self.symbol_dict = dict()
        for symbol in self.symbols:
            self.symbol_dict[str(symbol)] = EquationSymbol(name=str(symbol))

        for equation_symbol in equation_symbol_list:
            if equation_symbol.name in self.symbol_dict:
                self.symbol_dict[equation_symbol.name] = equation_symbol


    def findSymbols(self, eq):
        symbols = list()

        if isinstance(eq, Symbol):
            symbols.append(eq)
        else:
            for eqv in eq.args:
                symbols.extend(self.findSymbols(eqv))

        return symbols

    def calculate(self, symbol):
        eq = sympy.solve(self.sympy_equation, symbol)[0]
        for name, value in self.symbol_dict.items():
            eq = eq.subs(value.symbol, value.value)
        return eq.evalf()
