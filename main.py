from ABE import *
from time import time


if __name__ == '__main__':

    M = [random.randint(0, 2 ** 17) for i in range(256)]
    # print("************Message*****************")
    # print(M)

    # att_list = ['A','B','C','D']
    att_list = ['A', 'B']
    R = Setup(n, k, q, eta, att_list)

    userAttributes = ['A', 'B']

    sk = SKGen(R, userAttributes)
    # T = [['A','B'],['C','D']]
    T = [['A', 'B']]

    pk = PKGen(R, T, k, eta, q, n)

    # C = Enc(pk, M)
    # timeit(lambda: Enc(pk, M), '加密时间')
    # M_de = Decry(C, sk)
    # timeit(lambda: Decry(C, sk), '解密时间')
    #
    # print("************Decrypt Message*****************")
    # print(M_de)

    time1 = time()

    for j in range(100):
        C = Enc(pk, M)
        M_de = Decry(C, sk)

    print()
