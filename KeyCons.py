def KeyCons(Q: dict, T: list):
    """

    :param Q:
    :param T:
    :return:
    """

    n = len(Q[T[0]])
    m = len(Q[T[0]][0])

    s = [[0 for j in range(m)] for i in range(n)]
    for i in T:
        s = listAdd(s,Q[i])

    return s


def listAdd(l1: list, l2: list):
    n1 = len(l1)
    m1 = len(l1[0])

    n2 = len(l2)
    m2 = len(l2[0])

    assert n1 == n2 and m1 == m2

    l = [[0 for j in range(m1)] for i in range(n1)]

    for i in range(n1):
        for j in range(m1):
            l[i][j] = l1[i][j] + l2[i][j]

    return l



d = {}

d["A"] = [[0,1],[1,0]]
d["B"] = [[1,1],[1,1]]
d["C"] = [[1,0],[0,1]]

l = ["A","B"]

print(KeyCons(d,l))