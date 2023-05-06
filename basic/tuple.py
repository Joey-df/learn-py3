'''不可变序列，可变序列'''
'''可变序列  列表，字典'''
lst = [1, 2, 3]
print(id(lst))
lst.append(99)
print(id(lst))
'''不可变序列，字符串,元组'''
s = 'hello'
print(id(s))
s = s + 'world'
print(id(s))  # 生成了新的str
print(s)

'''元组的创建方式'''
'''第一种创建方式，使用()'''
t = ('Python', 'world', 98)
print(t)
print(type(t))  # <class 'tuple'>

t2 = 'Python', 'world', 98  # 省略了小括号
print(t2)
print(type(t2))  # <class 'tuple'>

t3 = ('Python',)  # 如果元组中只有一个元素，逗号不能省
print(t3)
print(type(t3))  # <class 'tuple'>

'''第二种创建方式，使用内置函数tuple()'''
t1 = tuple(('Python', 'world', 98))
print(t1)
print(type(t1))  # <class 'tuple'>

'''空元组的创建方式'''
'''空列表的创建方式'''
lst = []
lst1 = list()

d = {}
d2 = dict()

# 空元组
t4 = ()
t5 = tuple()
print('空列表', lst, lst1)
print('空字典', d, d2)
print('空元组', t4, t5)

'''tuple元素获取'''
# 和list一样使用[], 索引从0开始
t = (10, [20, 30], "Python")
print(t)
print(type(t))
print(t[0], type(t[0]), id(t[0]))
print(t[1], type(t[1]), id(t[1]))
print(t[2], type(t[2]), id(t[2]))
'''尝试将t[1]修改为100'''
# print(id(100))
# t[1] = 100  # TypeError: 'tuple' object does not support item assignment #元组是不允许修改元素的
'''由于[20,30]列表，而列表是可变序列，所以可以向列中添加元素，而列表的内存地址不变'''
t[1].append(100)  # 向列表中添加元素
print(t, id(t[1]))

'''元组的遍历'''
t = ('Python', 'world', 98)
'''第一种获取元组元组的方式，使用索引'''
print(t[0])
print(t[1])
print(t[2])
# print(t[3]) #IndexError: tuple index out of range
'''遍历元组'''
for item in t:
    print(item)

'''如果一个函数返回多个值，其实是一个tuple'''
def f():
    return 1, 2, 3
print(f())
