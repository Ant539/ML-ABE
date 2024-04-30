# from kyber_cpabe.params import KYBER_POLY_BYTES, KYBER_N, KYBER_ETAK512, KYBER_ETAK768_1024, KYBER_Q_INV, KYBER_Q
# from Crypto.Hash import SHAKE256
# from util import cast_to_byte
#
#
# def cast_to_byte(x):
#     y = x & 0xff
#     if y >= 2**7:
#         y -= 2**8
#     return y
#
# def convert_byte_to_32_bit_unsigned_int(x):
#     r = x[0] & 0xff # to mask negative values
#     r |= (x[1] & 0xff) << 8
#     r |= (x[2] & 0xff) << 16
#     r |= (x[3] & 0xff) << 24
#     return r
#
#
# def convert_byte_to_24_bit_unsigned_int(x):
#     r = x[0] & 0xff
#     r |= (x[1] & 0xff) << 8
#     r |= (x[2] & 0xff) << 16
#     return r
#
# def generate_prf_byte_array(l, key, nonce):
#     """
#     pseudo-random function to derive a deterministic array of random bytes
#     from the supplied secret key and a nonce
#     :param l: int (size of random byte array)
#     :param key: byte array
#     :param nonce: byte
#     :return: random byte array (hash)
#     """
#     hash = [ 0 for x in range(l)]
#     xof = SHAKE256.new()
#     new_key = [ 0 for x in range(0, len(key) + 1)]
#     for i in range(0, len(key)):
#         new_key[i] = key[i]
#     new_key[len(key)] = nonce
#     new_key = [ x & 0xff for x in new_key]
#     xof.update(bytearray(new_key))
#     hash = xof.read(l)
#     hash = [cast_to_byte(x) for x in hash ]
#     return hash

#
# def cbd(buf, paramsK):
#     r = [ 0 for x in range(0, KYBER_POLY_BYTES)]
#     if paramsK == 2:
#         for i in range(0, KYBER_N // 4):
#             t = convert_byte_to_24_bit_unsigned_int(buf[3 * i:])
#             d = t & 0x00249249
#             d = d + ((t >> 1) & 0x00249249)
#             d = d + ((t >> 2) & 0x00249249)
#             for j in range(0,4):
#                 a = ((d >> (6 * j + 0)) & 0x7)
#                 b = ((d >> (6 * j + KYBER_ETAK512)) & 0x7)
#                 r[4 * i + j] = (a - b)
#     else:
#         for i in range(0, KYBER_N // 8):
#             t = convert_byte_to_32_bit_unsigned_int(buf[4 * i:])
#             d = t & 0x55555555
#             d = d + ((t >> 1) & 0x55555555)
#             for j in range(0,8):
#                 a = ((d >> (4 * j + 0)) & 0x3)
#                 b = ((d >> (4 * j + KYBER_ETAK768_1024)) & 0x3)
#                 r[8 * i + j] = (a - b)
#     return r
#
#
# def get_noise_poly(seed, nonce, params_k):
#     l = None
#     if params_k == 2:
#         l = KYBER_ETAK512 * KYBER_N // 4
#     else:
#         l = KYBER_ETAK768_1024 * KYBER_N // 4
#     p = generate_prf_byte_array(l, seed, nonce)
#     return cbd(p, params_k)
import random

def bytes_to_bits(input_bytes):
    """
    Convert bytes to an array of bits

    Bytes are converted little endianness following the paper
    """
    bit_string = ''.join(format(byte, '08b')[::-1] for byte in input_bytes)
    return list(map(int, list(bit_string)))




def cbd(eta: int, k: int, n: int):
    """
    生成服从中心二项分布的随机数
    :param input_bytes: 二维数组，包含k个长度为n数组
    :param eta: 整数
    :param k: 整数，属性的数量
    :param n: 整数
    :return: 二维数组，包含k个长度为n数组
    """
    input_bytes = [[random.randint(0, 256) for j in range((n >> 2) * eta)] for i in range(k)]
    coefficients = [[0 for _ in range(n)] for _ in range(k)]
    for j in range(k):
        assert (n >> 2) * eta == len(input_bytes[j])

        list_of_bits = bytes_to_bits(input_bytes[j])
        for i in range(n):
            a = sum(list_of_bits[2 * i * eta + j] for j in range(eta))
            b = sum(list_of_bits[2 * i * eta + eta + j] for j in range(eta))
            coefficients[j][i] = a - b
    return coefficients

# len(test_array) == 128
# test_array = [[-10, -42, -45, -5, -122, -36, 94, 111, -22, 89, 53, -127, 127, 87, 32, 62, -113, 7, -118, -18, -125, 9, -112, 56, 72, -28, -124, 26, -24, 87, 114, 109, -72, 96, 123, -31, -119, 106, 22, 120, 19, 101, -30, -65, 75, -65, -2, 4, 118, 18, -24, -3, 6, -8, -50, 48, -99, -71, -63, 44, -30, 57, 29, 125, -27, -54, 98, -41, -2, -61, -59, -103, 127, -102, 1, 12, 81, -9, 75, 118, -11, 117, 87, -117, 8, -102, -6, -74, -9, -80, 30, -37, -87, -83, -113, -14, 20, 78, 92, 38, 54, -18, -56, 78, 39, 87, -26, 115, 89, -22, 125, -14, -85, 82, -101, 104, -91, 75, 92, -73, 37, 44, 13, 84, -114, -23, 126, 112]]
# # test_array值在0-255
# for i in range(len(test_array)):
#     for j in range(len(test_array[i])):
#         test_array[i][j] += 127
#
# res = cbd(test_array, 2, 1, 256)
# print(res)