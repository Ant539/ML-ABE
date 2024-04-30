from CBD import cbd
from Compress import Compress, Decompress
import random
from util import *
from KeyCons import KeyCons
from params import n, k, q, eta



def Setup(n: int, k: int, q: int, eta: int, attributeSet: list, seed=1):
    """
    生成每个属性对应的密钥参数集

    :param n: kyber n
    :param k: kyber k
    :param q: 质数
    :param eta:
    :param attributeSet: 总属性列表
    :param seed: 随机数种子
    :return: 字典："属性" : "密钥参数"。
    ——————————————（1） R ——————————————————
    R是私钥字典，其键为属性值，例如A B C D等，对应的值通过中心二项式分布得到，长度为k的列表，
    每一列表元素为一个n次的多项式（即一个长度为n的子列表）
    ——————————————（2）CBD 函数——————————————

    """

    R = {}
    random.seed(seed)
    for i in range(len(attributeSet)):
        R[attributeSet[i]] = cbd(eta, k, n)
    return R


# n = 256
# k = 2
# q = 3329




def SKGen(R: dict, userAttributes: list):
    """
    根据用户的属性列表生成用户私钥

    :param R: 密钥参数字典
    :param userAttributes: 用户属性集合
    :return: 用户私钥字典: "用户属性" : "涉及用户属性的密钥参数"
    此处返回的私钥，是根据Setup中存储的字典R进行查找，寻找用户的属性对应的，
    """
    sk = {}
    for userAttribute in userAttributes:
        assert userAttribute in R, "user attribute is invalid, please check again"
        sk[userAttribute] = R[userAttribute]
    return sk
#
# sk = SKGen(R,userAttributes)
# print(len(sk['D'][0]))


def PKGen(R:dict, T: list, k: int, eta: int, q: int, n: int, seed = 1):
    """

    :param R: 密钥参数字典
    :param T: 访问策略树：访问策略是为析取式，该T包含的每个列表表示一个范式中的属性
    :param k: kyber k
    :param eta: kyber eta
    :param q: 质数
    :param n: kyber n
    :param seed: 随机数种子
    :return:
    """
    random.seed(seed)
    A = [[[random.randint(0, q) for _ in range(n)] for _ in range(k)] for _ in range(k)]
    t = {}

    for key, value in R.items():
        ei = cbd(eta, k, n)
        Ari = matrix_vector_poly_mul(A, value)
        t[key] = Compress(poly_add(Ari, ei).tolist(), q, 27)

    pk = {}
    pk["A"] = A
    pk["T"] = t
    return pk




def Enc(pk, M, W, q, PIE):


    A = pk['A']
    ti = {}
    z = []
    t = pk["T"]
    for key,value in t.items():
        ti[key] = Decompress(t[key], q, 27)
    c = []
    v = []
    for attribute in PIE:

        attrs = ["A"]
        for attr in attrs:
            v.append(cbd(eta, 3, 256))
           # v.append(cbd(3, 3, 256))
        ei = cbd(eta, 1, 256)
        c0 = poly_dotprod(ti[attribute], v[0]).tolist()
        round_q = round(q / (2 ** 17))
        M_q = [round_q * item for item in M]
        c.append(poly_add(poly_add(c0,ei[0]).tolist(), M_q).tolist())

    lambdai = []
    lambdai.append(v[0])
    #lambdai.append(matrix_sub(v[0], v[1]))

    e2 = cbd(eta,3,256)
    z.append(poly_add(matrix_vector_poly_mul(A, lambdai[0]), e2).tolist())
    # e2 = cbd(3, 3, 256)
    # z.append(matrix_addition(matrix_vector_poly_mul(A, transpose(lambdai[1])), e2))
    c1 = Compress(c,q,21)
    c2 = []
    c2.append(Compress(z[0],q,28))
    # c2.append(Compress(z[1],q,28))

    C = {}
    C['c1'] = c1
    C['c2'] = c2

    return C


def Decry(C, sk):

    c1 = C['c1']
    c2 = C['c2']


    c = Decompress(c1, q ,21)
    z1 = Decompress(c2[0], q,28)
    # z2 = Decompress(c2[1], q,28)
    w = []
    w.append(poly_dotprod(z1,sk["A"]))
    # w.append(poly_dotprod(z2, sk["A"]))

    # c11 = poly_add(w[0]).tolist()
    # test = poly_sub(c[0], w[0]).tolist()
    c_s_w = [a - b for a, b in zip(c[0], w[0])]
    # M_de = Compress(poly_sub(c[0], w[0]).tolist(), q, 17)
    M_de = Compress(c_s_w, q, 17)
    # print("c1 - w1",Compress(poly_sub(c[1],w[1]).tolist(), q, 17))
    # print("c0 - w0",Compress(poly_sub(c[0],w[0]).tolist(), q, 17))


    return M_de



W = [[1]]
PIE = ['A']






M = [random.randint(0, 2 ** 17) for i in range(256)]
print("************Message*****************")
print(M)

# att_list = ['A','B','C','D']
att_list = ['A']
R = Setup(n, k, q, eta, att_list)

userAttributes = ['A']

sk = SKGen(R, userAttributes)
# T = [['A','B'],['C','D']]
T = [['A']]

pk = PKGen(R, T, k, eta, q, n)

C = Enc(pk, M,W,q,PIE)
# timeit(lambda: Enc(pk, M,W,q,PIE), '加密时间')
M_de = Decry(C, sk)
# timeit(lambda: Decry(C, sk), '解密时间')

print("************Decrypt Message*****************")
print(M_de)




