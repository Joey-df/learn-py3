# https://docs.python.org/zh-cn/3/library/stdtypes.html#sequence-types-list-tuple-range
'''输出一个三行四列的矩形'''
for i in range(1, 4):  # 行表，执行三次，一次是一行
    for j in range(1, 5):
        print('*', end='\t')  # 不换行输出
    print()  # 打行

# range()的三种创建方式
'''第一种创建方式，只有一个参数（小括号中只给了一个数）'''
r = range(10)  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],默认从0开始，默认相差1称为步长
print(r)  # range(0, 10)
print(list(r))  # 用于查看range对象中的整数序列    -->list是列表的意思

'''第二种创建方式，给了两个参数（小括号中给了两个数）'''
r = range(1, 10)  # 指定了起始值，从1开始，到10结束（不包含10），默认步长为1
print(list(r))  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

'''第三种创建方式，给了三个参数（小括号中给了三个数）'''
r = range(1, 10, 2)
print(list(r))  # [1, 3, 5, 7, 9]

'''判断指定的整数 在序列中是否存在 in ,not in'''
print(10 in r)  # False ,10不在当前的r这个整数序列中
print(9 in r)  # True,9在当关的r这个序列中

print(10 not in r)  # True
print(9 not in r)  # False

print(range(1, 20, 1))  # range(1, 20)
print(list(range(1, 20, 1)))  # [1...19]
print(range(1, 101, 1))  # range(1, 101)
print(list(range(1, 101, 1)))  # list 1~100

print(list(range(-10, -100, -30)))  # [-10, -40, -70]
