from params import *
from Crypto.Hash import SHAKE128, SHAKE256
import random
import numpy as np
import time

def can_add(matrix1, matrix2):
    """
    Returns True if two matrices can be added.
    """
    return len(matrix1) == len(matrix2) and len(matrix1[0]) == len(matrix2[0])


def can_multiply(matrix1, matrix2):
    """
    Returns True if two matrices can be multiplied.
    """
    return len(matrix1[0]) == len(matrix2)


def matrix_addition(matrix1, matrix2):
    """
    Adds two matrices element-wise.
    """
    # assert can_add(matrix1, matrix2)
    result = []
    for i in range(len(matrix1)):
        row = []
        for j in range(len(matrix1[0])):
            row.append(matrix1[i][j] + matrix2[i][j])
        row = poly_mod(np.array(row))
        result.append(row.tolist())
    return result

def matrix_sub(matrix1, matrix2):
    """
    Subs two matrices element-wise.
    """
    # assert can_add(matrix1, matrix2)
    result = []
    for i in range(len(matrix1)):
        row = []
        for j in range(len(matrix1[0])):
            row.append(matrix1[i][j] - matrix2[i][j])
        row = poly_mod(np.array(row))
        result.append(row.tolist())
    return result


def matrix_multiplication(matrix1, matrix2):
    """
    Multiplies two matrices.
    """
    assert can_multiply(matrix1, matrix2)
    result = []
    for i in range(len(matrix1)):
        row = []
        for j in range(len(matrix2[0])):
            sum = 0
            for k in range(len(matrix2)):
                sum += matrix1[i][k] * matrix2[k][j]
            row.append(sum)
        result.append(row)
    return result

#  A uniformly randow polynomial matrix


def transpose(A):
    transposed = []

    for i in range(len(A[0])):
        row = []

        for j in range(len(A)):
            row.append(A[j][i])

        transposed.append(row)

    return transposed


# print(A)
# print(transpose(A))


def poly_mod(exp):
    """
    expression (mod (x^f + 1))
    """
    m = len(exp)
    res = exp % q
    for i in range(0, m-n):
        d = res[i]
        res[i] -= d
        res[i + n] -= d
    res = res[-n:] % q
    return res


def poly_add(s1, s2):
    """
        t = s1 + s2
    """
    return poly_mod(np.polyadd(s1, s2))  # 多项式相加


def poly_sub(s1, s2):
    """
        t = s1 + s2
    """
    return poly_mod(np.polysub(s1, s2))  # 多项式相加


def poly_mul(s1, s2):
    """
        t = s1 * s2
    """
    return poly_mod(np.convolve(s1, s2))  # convolve：卷积


def poly_dotprod(s1, s2):
    """
        t = s1[0]*s2[0] + s1[1]*s2[1] ... + s1[m-1]*s2[m-1]
    """
    n_poly = np.array([poly_mul(np.array(poly)[0], np.array(poly)[1])
                       for poly in zip(s1, s2)])
    n = [0]
    for j in n_poly:
        n = poly_add(n, j)

    return n


def matrix_vector_poly_mul(A, s):
    result = []

    for row in A:
        sum_poly = [0] * max(len(row[0]), len(s[0]))  # initialize a polynomial with zeros

        for i in range(len(row)):
            product = poly_mul(row[i], s[i])
            sum_poly = poly_add(sum_poly, product)

        result.append(sum_poly.tolist())

    return result

def timeit(code, title):
    st = time.time()
    res = code()
    end = time.time()
    t = round(end - st, 10)
    print(title, '-', t, '(s)')
    print("{}-{:.8f}(s)".format(title,t))
    return res

#
# A = [[[1,2],[3,4]],[[5,6],[7,8]]]
# s = [[1,2],[3,4]]
# print(matrix_vector_poly_mul(A,s))

# s1 = [1,2]
#
# s2 = [3,4]
#
# print(poly_add(poly_mul(s1,s1),poly_mul(s2,s2)))
#
# a = np.array([26,68,44])
# print(poly_mod(a))