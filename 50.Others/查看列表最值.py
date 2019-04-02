def findmaxvalue(list1):
    maxvalue = list1[0]
    minvalue = list1[0]
    for i in list1:
        if i > maxvalue:
            maxvalue = i
        elif i < minvalue:
            minvalue = i
    result = (maxvalue, minvalue)
    return result


List = [1, 3, 15, 20, 50, -5, 123, 5]
value = findmaxvalue(List)
print("最大值和最小值分别为：" + str(value[0]) + "," + str(value[1]))
