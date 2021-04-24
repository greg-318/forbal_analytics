


list = [20.22, 58.86, 20.92]

list1 = [45.35, 45.35, 9.30]

b = [int(num+0.5) for num in list]
if sum(b) < 100:
    b[1] += 1


print(b)




result = []
balance = []
for item in list:
    item_str = str(item)
    value = item_str.split('.')
    result.append(int(value[0]))
    balance.append(int(value[1]))

while 100 - sum(result) != 0:
    index = balance.index(max(balance))
    balance.pop(index)
    result[index] += 1








