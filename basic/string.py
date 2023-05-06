# 字符串的驻留机制
a = 'Python'
b = "Python"
c = '''Python'''
print(a, id(a))
print(b, id(b))
print(c, id(c))
print(id(a) == id(b) == id(c))  # Ture
print(a is b is c)  # Ture

s1 = 'abc%'
s2 = 'abc%'
print(s1 is s2)  # True


# 字符串的查询操作
s = 'hello,hello'
print(s.index('lo'))  # 3
print(s.find('lo'))  # 3
print(s.rindex('lo'))  # 9
print(s.rfind('lo'))  # 9

# print(s.index('k')) #ValueError: substring not found
print(s.find('k'))  # -1
# print(s.rindex('k')) #ValueError: substring not found
print(s.rfind('k'))  # -1


# 字符串中的大小写转换的方法
s = 'hello,python'
a = s.upper()  # 转成大写之后，会产生一个新的字符串对象
print(a, id(a))
print(s, id(s))
b = s.lower()  # 转换之后，会产生一个新的字符串对象
print(b, id(b))
print(s, id(s))
print(b == s)
print(b is s)  # False

s2 = 'hello,Python'
print(s2.swapcase())
print(s2.title())  # 每个单词首字母变大写

# 字符串对齐
s = 'hello,Python'
'''居中对齐'''
print(s.center(20, '*'))

'''左对齐'''
print(s.ljust(20, '*'))
print(s.ljust(2))
print(s.ljust(20))

'''右对齐'''
print(s.rjust(20, '*'))
print(s.rjust(80))
print(s.rjust(10))

'''右对齐，使用0进行填充'''
print(s.zfill(20))
print(s.zfill(10))
print('-8910'.zfill(8))


# 字符串切分
s = 'hello world Python'
lst = s.split()
print(lst)
s1 = 'hello|world|Python'
print(s1.split(sep='|'))
print(s1.split(sep='|', maxsplit=1))
print('-------------------------------')
'''rsplit()从右侧开始劈分'''
print(s.rsplit())
print(s1.rsplit('|'))
print(s1.rsplit(sep='|', maxsplit=1))


# 标识符判断
s = 'hello,python'
print('1.', s.isidentifier())  # False
print('2.', 'hello'.isidentifier())  # True
print('3.', '张三_'.isidentifier())  # True
print('4.', '张三_123'.isidentifier())  # True

print('5.', '\t'.isspace())  # True

print('6.', 'abc'.isalpha())  # True
print('7.', '张三'.isalpha())  # True
print('8.', '张三1'.isalpha())  # False

print('9.', '123'.isdecimal())  # True
print('10.', '123四'.isdecimal())  # False
print('11.', 'ⅡⅡⅡ'.isdecimal())  # False

print('12.', '123'.isnumeric())  # True
print('13.', '123四'.isnumeric())  # True
print('14.', 'ⅡⅡⅡ'.isnumeric())  # True

print('15.', 'abc1'.isalnum())  # True
print('16.', '张三123'.isalnum())  # True
print('17.', 'abc!'.isalnum())  # False


# 字符串替换与连接
s = 'hello,Python'
print(s.replace('Python', 'Java'))  # hello,Java
s1 = 'hello,Python,Python,Python'
print(s1.replace('Python', 'Java', 2))  # hello,Java,Java,Python

lst = ['hello', 'java', 'Python']
print('|'.join(lst))  # hello|java|Python
print(','.join(lst))  # hello,java,Python

t = ('hello', 'Java', 'Python')
print('-'.join(t))  # hello-Java-Python

print('*'.join('Python'))  # P*y*t*h*o*n


# 字符串比较
print('apple' > 'app')  # True
print('apple' > 'banana')  # False，相当于97>98
print(ord('a'), ord('b'))
print(ord('杨'))

print(chr(97), chr(98))
print(chr(26472))

'''== 与is的区别
  == 比较的是 value
  is  比较的是id是否相等'''
a = b = 'Python'
c = 'Python'
print(a == b)  # True
print(b == c)  # True

print(a is b)  # True
print(a is c)  # True
print(a is b is c)  # True
print(id(a) == id(b) == id(c))  # True


# slice操作
s = 'hello,Python'
s1 = s[:5]  # hello 由于没有指定起始位置，所以从0开始切
s2 = s[6:]  # Python 由于没有指定结束位置，所以切到字符串的最后一个元素
s3 = '!'
new_str = s1 + s3 + s2 #hello!Python

print(s1)
print(s2)
print(new_str)
print('--------------------')
print(id(s))
print(id(s1))
print(id(s2))
print(id(s3))
print(id(new_str))

print('------------------切片[start:end:step]-------------------------')
print(s[1:5:1])  # 从1开始截到5（不包含5），步长为1
print(s[::2])  # 默认从0 开始，没有写结束，默认到字符串的最后一个元素 ,步长为2  ，两个元素之间的索引间隔为2
print(s[::-1])  # 默认从字符串的最后一个元素开始，到字符串的第一个元素结束，因为步长为负数
print(s[-6::1])  # 从索引为-6开始，到字符串的最后一个元素结束，步长为1


# 格式化字符串
# (1) % 占位符
name = '张三'
age = 20
print('我叫%s,今年%d岁' % (name, age))

# (2) {}
print('我叫{0},今年{1}岁，我真的叫 {0}'.format(name, age))  # 带占位符，下标从0开始
print('我叫{},今年{}岁'.format(name, age))  # 也可以不带占位符

# (3)f-string
print(f'我叫{name},今年{age}岁')

# 格式化输出，带宽度和精度（可以使用%或者{}两种方式）
print('%d' % 99)
print('%10d' % 99)  # 10表示的是宽度
print('%.3f' % 3.1415926)  # .3表示是小数点后三位
# 同时表示宽度和精度
print('%10.3f' % 3.1415926)  # 一共总宽度为10，小数点后 3位
print('hellohello')  # 长度为10
print('{0:.3}'.format(3.1415926))  # .3表示的是一共是3位数【0表示的是占位符/下标，可以省略】
print('{0:.3},    {1:.4}'.format(3.1415926, 3.1415926))
print('{:.3},    {:.4}'.format(3.1415926, 3.1415926))
print('{:.3}'.format(3.1415926))  # .3表示的是一共是3位数
print('{:.3f}'.format(3.1415926))  # .3f表示是3位小数
print('{:10.3f}'.format(3.1415926))  # 同时设置宽度和精度，一共是10位，3位是小数
print('hellohello')  # 长度为10


# 编码与解码
s = '天涯共此时'
# 编码
print(s.encode(encoding='GBK'))  # 在GBK这种编码格中 一个中文占两个字节
print(s.encode(encoding='UTF-8'))  # 在UTF-8这种编辑格式中，一个中文占三个字节

# 解码
# byte代表就是一个二进制数据（字节类型的数据）
byte = s.encode(encoding='GBK')  # 编码
print(byte.decode(encoding='GBK'))  # 解码

byte = s.encode(encoding='UTF-8')
print(byte.decode(encoding='UTF-8'))
