# for
words = ['cat', 'window', 'defenestrate']
for w in words:
    print(w, len(w))

'''
循环中的 break、continue 语句及 else 子句
break 语句和 C 中的类似，用于跳出最近的 for 或 while 循环。
循环语句支持 else 子句；for 循环中，可迭代对象中的元素全部循环完毕，或 while 循环的条件为假时，执行该子句；break 语句终止循环时，不执行该子句。 
请看下面这个查找素数的循环示例：
'''
# for - else
for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print(n, 'equals', x, '*', n // x)
            break
    else:
        # loop fell through without finding a factor
        print(n, 'is a prime number')

for item in range(3):
    pwd = input('请输入密码:')
    if pwd == '8888':
        print('密码正确')
        break
    else:
        print('密码不正确')
else:
    print('对不起，三次密码均输入错误')

'''
while4步循环法：
 1.初始化变量
 2.条件判断
 3.条件执行体（循环体）
 4.改变变量
 总结： 初始化的变量与条件判断的变量与改变的变量为同一个
'''
a = 0  # 初始化变量
while a < 3:  # 条件判断
    '''条件执行体（循环体)'''
    pwd = input('请输入密码')
    if pwd == '8888':
        print('密码正确')
        break
    else:
        print('密码不正确')
    '''改变变量'''
    a += 1
else:  # while - else
    print('对不起，三次密码均输入错误')

'''continue 语句也借鉴自 C 语言，表示继续执行循环的下一次迭代：'''
for num in range(2, 10):
    if num % 2 == 0:
        print("Found an even number", num)
        continue
    print("Found an odd number", num)

for item in 'Python':  # 第一次取出来的是P,将P赋值值item,将item的值输出
    print(item)

# range() 产生一个整数序列，也是一个可迭代对象
for i in range(10):
    print(i)

# 如果在循环体中不需要使用到自定义变量，可将自定义变量写为“_”
for _ in range(5):
    print('人生苦短，我用Python')

'''使用for循环，计算1到100之间的偶数和'''
sum = 0  # 用于存储偶数和
for item in range(1, 101):
    if item % 2 == 0:
        sum += item
print('1到100之间的偶数和为:', sum)

'''输出100到999之间的水仙花数
   举例: 153=3*3*3+5*5*5+1*1*1
'''
for item in range(100, 1000):
    g = item % 10  # 个位
    s = item // 10 % 10  # 十位
    b = item // 100  # 百位
    # print(bai,shi,ge)
    # 判断
    if g ** 3 + s ** 3 + b ** 3 == item:
        print(item)

'''九九乘法表'''
for i in range(1, 10):  # 行数
    for j in range(1, i + 1):
        print(i, '*', j, '=', i * j, end='\t')
    print()  # 换行
