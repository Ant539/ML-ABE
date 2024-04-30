# Compress for list only
# def Compress(x_list: list, q: int, d: int):
#     compressed_list = []
#     for sub_list in x_list:
#         compressed_sub_list = [(2 ** d / q) * x for x in sub_list]
#         compressed_sub_list = [round(x) % (2 ** d) for x in compressed_sub_list]
#         compressed_list.append(compressed_sub_list)
#     return compressed_list
import random


def Compress(x_list: list, q: int, d: int):
    compressed_list = []
    for ele in x_list:
        if isinstance(ele, list):  # 出现子列表
            sub_list = ele
        else:
            sub_list = x_list  # 没有子列表，直接使用整个列表
            compressed_sub_list = [(2 ** d / q) * x for x in sub_list]
            compressed_sub_list = [round(x) % (2 ** d) for x in compressed_sub_list]
            compressed_list.append(compressed_sub_list)
            break

        compressed_sub_list = [(2 ** d / q) * x for x in sub_list]
        compressed_sub_list = [round(x) % (2 ** d) for x in compressed_sub_list]
        compressed_list.append(compressed_sub_list)
    return compressed_list


def Decompress(x_list: list, q: int, d: int):
    decompressed_list = []
    for ele in x_list:
        if isinstance(ele, list):  # 出现子列表
            sub_list = ele
        else:
            sub_list = x_list  # 没有子列表，直接使用整个列表
            decompressed_sub_list = [(q / (2 ** d)) * x for x in sub_list]
            decompressed_sub_list = [round(x) for x in decompressed_sub_list]
            decompressed_list.append(decompressed_sub_list)
            break  # 直接退出循环，以防止额外的迭代

        decompressed_sub_list = [(q / (2 ** d)) * x for x in sub_list]
        decompressed_sub_list = [round(x) for x in decompressed_sub_list]
        decompressed_list.append(decompressed_sub_list)

    return decompressed_list

