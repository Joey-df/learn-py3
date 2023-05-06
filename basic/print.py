# 可以输出数字
print(520)
print(98.5)

# 可以输出字符串
print('helloworld')
print("helloworld")
print('''helloworld''')
print("""helloworld""")

# 含有运算符的表达式
print(3 + 1)

# 将数据输出文件中:
# 注意点，1，所指定的盘符须存在（不写盘符默认在当前目录），2.使用file=fp
fp = open('text.txt', 'a+')  # a+如果文件不存在就创建，存在就在文件内容的后面继续追加
print('helloworld', file=fp)
fp.close()

with open("text.txt", mode='a+') as f:
    print('hello world', file=f)

# 不进行换行输出（输出内容在一行当中）
print('hello', 'world', 'Python')

"""
转义字符 \ + 转义功能的首字母   n-->newline的首字符表示换行
"""
print('hello\nworld')
print('hello\tworld')
print('helloooo\tworld')
print('hello\rworld')  # world将hello进行了覆盖
print('hello\bworld')  # \b是退一个格，将o退没了

print('http://www.baidu.com')
print("\\\\")  # 输出\\
print('老师说:\'大家好\'')

# 原字符，不希望字符串中的转义字符起作用，就使用原字符，就是在字符串之前加上r,或R
print(r'hello\nworld')
print(R'hello\nworld')
# 注意事项， 最后一个字符不能是反斜杠
# print(r'hello\nworld\')
print(r'hello\nworld\\')

# 字符编码
print(chr(0b100111001011000))
print(ord('乘'))

name = '马丽亚'
print(f'标识: {id(name)}, 类型: {type(name)}, 值: {name}')

# 整数类型
# 可以表示，正数，负数， 0
n1 = 90
n2 = -76
n3 = 0
print(n1, type(n1))
print(n2, type(n2))
print(n3, type(n3))
# 整数可以表示为二进制，十进制，八进制，十六进制
print('十进制', 118)
print('二进制', 0b10101111)  # 二进制以0b开头
print('八进制', 0o176)  # 八进制以0o开头
print('十六进制', 0x1EAF)

a = 3.14159
print(a, type(a))  # 3.14159 <class 'float'>
n1 = 1.1
n2 = 2.2
n3 = 2.1
print(n1 + n2)  # 输出3.3000000000000003
print(n1 + n3)  # 输出3.2
from decimal import Decimal

print(Decimal('1.1') + Decimal('2.2'))  # 输出3.3

f1 = True
f2 = False
print(f1, type(f1))
print(f2, type(f2))
# 布尔值可以转成整数计算
print(f1 + 1)  # 输出2  1+1的结果为2, True表示1
print(f2 + 1)  # 输出1  0+1的结果为1, False表示0

str1 = '人生苦短，我用Python'
str2 = "人生苦短，我用Python"
str3 = """人生苦短，
我用Python"""
str4 = '''人生苦短，
我用Python'''
print(str1, type(str1))
print(str2, type(str2))
print(str3, type(str3))
print(str4, type(str4))

# 数据类型转换
print("-------数据类型转换-------------")
name = '张三'
age = 20

print(type(name), type(age))  # 说明name与age的数据类型不相同
# print('我叫'+name+'今年,'+age+'岁')  #当将str类型与int类型进行连接时，报错，解决方案，类型转换
print('我叫' + name + '今年,' + str(age) + '岁')  # 将int类型通过str()函数转成了str类型

print('----------------str()将其它类型转成str类型---')
a = 10
b = 198.8
c = False
print(type(a), type(b), type(c))
print(str(a), str(b), str(c), type(str(a)), type(str(b)), type(str(c)))

print('----------int()将其它的类型转int类型-----------------')
s1 = '128'
f1 = 98.7
s2 = '76.77'
ff = True
s3 = 'hello'
print(type(s1), type(f1), type(s2), type(ff), type(s3))
print(int(s1), type(int(s1)))  # 将str转成int类型 ,字符串为 数字串
print(int(f1), type(int(f1)))  # float转成int类型，截取整数部分，舍掉小数部分
# print(int(s2),type(int(s2)))  #将str转成int类型，报错，因为字符串为小数串
print(int(ff), type(int(ff)))
# print(int(s3),type(int(s3)))  #将str转成int类型时，字符串必须为数字串（整数），非数字串是不允许转换

print('------------float()函数，将其它数据类型转成float类型')

s1 = '128.98'
s2 = '76'
ff = True
s3 = 'hello'
i = 98
print(type(s1), type(s2), type(ff), type(s3), type(i))
print(float(s1), type(float(s1)))
print(float(s2), type(float(s2)))
print(float(ff), type(float(ff)))
# print(float(s3),type(float(s3))) #字符串中的数据如果是非数字串，则不允许转换
print(float(i), type(float(i)))

'''嘿嘿，
我是
多行注释'''
import keyword

print(keyword.kwlist)  # 打印python的关键字列表
