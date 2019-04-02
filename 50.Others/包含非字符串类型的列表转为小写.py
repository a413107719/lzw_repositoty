list2 = ['Hello', 'World', 18, 'Apple', None]
listlower = []
for i in list2:
    if isinstance(i, str):
        listlower.append(i.lower())
    else:
        listlower.append(i)
print(listlower)




