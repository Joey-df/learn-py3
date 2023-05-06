# 集合的创建方式

'''第一种创建方式使用{}'''
s = {2, 3, 4, 5, 5, 6, 7, 7}  # 集合中的元素不允许重复
print(s)

'''第二种创建方式使用set(),其中可以传入list，tuple，set'''
s1 = set(range(6))
print(s1, type(s1))

s2 = set([1, 2, 4, 5, 5, 5, 6, 6])
print(s2, type(s2))

s3 = set((1, 2, 4, 4, 5, 65))  # 集合中的元素是元序的
print(s3, type(s3))

s4 = set('python')
print(s4, type(s4))  # {'n', 'p', 'o', 'h', 't', 'y'} <class 'set'>

s5 = set({12, 4, 34, 55, 66, 44, 4})
print(s5, type(s5))

# 定义一个空集合
s6 = {}  # dict字典类型
print(type(s6))  # <class 'dict'>

s7 = set()
print(type(s7))  # <class 'set'>



# 集合的相关操作
s = {1, 2, 3}
'''集合元素的判断操作'''
print(1 in s)  # True
print(100 in s)  # False
print(1 not in s)  # False
print(100 not in s)  # True
'''集合元素的新增操作'''
s.add(80)  # add一次添加一个元素
print(s)  # {80, 1, 2, 3}
s.update({22, 33, 44})  # 一次至少添加一个元素
print(s)  # {80, 1, 2, 3, 33, 22, 44}
s.update(['hi', 'py3'])
s.update((100, 200))
print(s)  # {1, 2, 3, 200, 80, 22, 33, 'hi', 100, 44, 'py3'}

'''集合元素的删除操作'''
s.remove(100)
print(s)  # {1, 2, 3, 200, 80, 22, 'hi', 33, 'py3', 44}
# s.remove(500) #KeyError: 500
s.discard(500)  # Remove if it is a member, otherwise do nothing
s.discard(200)
print(s)  # {1, 2, 3, 80, 22, 'hi', 33, 'py3', 44}
s.pop()  # Remove and return an arbitrary set element. Raises KeyError if the set is empty.
s.pop()

# s.pop(400) #TypeError: pop() takes no arguments (1 given)
print(s)
s.clear()
print(s)  # set()



'''两个集合是否相等（元素相同，就相等）'''
s = {10, 20, 30, 40}
s2 = {30, 40, 20, 10}
print(s == s2)  # True
print(s != s2)  # False

'''一个集合是否是另一个集合的子集'''
s1 = {10, 20, 30, 40, 50, 60}
s2 = {10, 20, 30, 40}
s3 = {10, 20, 90}
print(s2.issubset(s1))  # True
print(s3.issubset(s1))  # False

'''一个集合是否是另一个集合的超集'''
print(s1.issuperset(s2))  # True
print(s1.issuperset(s3))  # False

'''两个集合是否含有交集'''
print(s2.isdisjoint(s3))  # False   有交集为False
s4 = {100, 200, 300}

print(s2.isdisjoint(s4))  # True    没有交集为True


# 集合的数学操作
s1 = {10, 20, 30, 40}
s2 = {20, 30, 40, 50, 60}
print(f"s1：{s1}\ns2：{s2}")

# （1）交集
print("交集:")
print(s1.intersection(s2)) # {40, 20, 30}
print(s1 & s2)  # {40, 20, 30} intersection()与 & 等价，交集操作

# (2)并集操作
print("并集:")
print(s1.union(s2)) # {40, 10, 50, 20, 60, 30}
print(s1 | s2)  # union与  | 等价，并集操作

# (3)差集操作
print("差集:")
print(s1.difference(s2)) # {10}
print(s1 - s2) # {10}

# （4）对称差集
print("对称差集:")
print(s1.symmetric_difference(s2))
print(s1 ^ s2)


# 集合生成式
print("集合生成式: ")
s = {i + 10 for i in range(10)}
print(s)
