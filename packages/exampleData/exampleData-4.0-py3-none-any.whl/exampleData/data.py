import requests
import math
import numpy as np

'''
CHAPTER 1: System of Linear Algebraic Equations
CHAPTER 2: Eigenproblems
CHAPTER 3: Nonlinear Equations
CHAPTER 4: Polynomial Approximation and Interpolation
CHAPTER 5: Numerical Differentiation and Difference Formulas
CHAPTER 6: Numerical Integration
CHAPTER 7: Ordinary Differential Equations

'''
chap_1 = 'https://numerical-matrix-example.nguyncng4.repl.co/chapter-1'
chap_2 = 'https://numerical-matrix-example.nguyncng4.repl.co/chapter-2'
chap_3 = 'https://numerical-matrix-example.nguyncng4.repl.co/chapter-3'
chap_4 = 'https://numerical-matrix-example.nguyncng4.repl.co/'
chap_5 = 'https://numerical-matrix-example.nguyncng4.repl.co/'
chap_6 = 'https://numerical-matrix-example.nguyncng4.repl.co/'
chap_7 = 'https://numerical-matrix-example.nguyncng4.repl.co/'


def get_chapter_1():
    '''
    return a dictionary of matrices
    '''
    response = requests.get(chap_1)
    data = response.json()
    matrix = dict(data)
    for key in matrix:
        if ismatrix(matrix[key]):
            matrix[key] = np.matrix(matrix[key], dtype=float)
        else:
            for subkey in matrix[key]:
                matrix[key][subkey] = np.array(matrix[key][subkey], dtype=float)
    return matrix

def get_chapter_2():
    '''
    return a dictionary of matrices
    '''
    response = requests.get(chap_2)
    data = response.json()
    matrix = dict(data)
    for key in matrix:
        matrix[key] = np.array(matrix[key], dtype=float)
    return matrix

def get_chapter_3():
    '''
    return a dictionary of functions
    '''
    response = requests.get(chap_3)
    data = response.json()
    nlinear_func = dict(data)
    func_str = nlinear_func.copy()
    for key in nlinear_func:
        nlinear_func[key] = "def " + key + "(x): return " + nlinear_func[key]

    func_dict = {}
    for key in nlinear_func:
        exec(str(nlinear_func[key]), globals())
        func_dict[key] = eval(key)
    return func_dict, func_str

def ismatrix(A):
    if type(A) != list or len(A) == 0:
        return False
    n = len(A[0])
    for row in A:
        if type(row) != list or len(row) != n:
            return False
    return True

def get_chapter_4():
    pass

def get_chapter_5():
    pass

def get_chapter_6():
    pass

def get_chapter_7():
    pass