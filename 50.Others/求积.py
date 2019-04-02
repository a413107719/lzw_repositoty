from functools import reduce

def prod(x,y):
    return x * y


def function(L):
    a = reduce(prod, L)
    print(a)


list1 = [1, 2, 3, 4, 5, 6, 7]
function(list1)