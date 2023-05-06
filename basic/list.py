# 创建列表
'''创建列表的第一种方式，使用[]'''
print("----list创建与元素获取----")
lst = ['hello', 'world', 98, 'Python']
print(lst)
print(lst[0], lst[-4], lst[-1])  # 按照下标获取
print(id(lst[0]), id(lst[-4]))
# 获取索引为10的元素
# print(lst[10])  # IndexError: list index out of range
'''创建列表的第二种方式，使用内置函数list()'''
lst2 = list(['hello', 'world', 98])
print(lst2)

'''slice操作'''
print("------------slice操作-------------")
lst = [0, 1, 2, 3, 4, 5, 6, 7]
# start=1,stop=6,step=1
print(lst[1:6:1])  # [start, stop)
print('原列表id:', id(lst))
lst2 = lst[1:6:1]
print('切的片段id:', id(lst2))
print(lst[1:6])  # 默认步长为1
print(lst[1:6:])
# start=1,stop=6,step=2
print(lst[1:6:2])
# stop=6,step=2,start采用默认
print(lst[:6:2])
# start=1，step=2，stop采用默认
print(lst[1::2])
print('------------step步长为负数的情况---------------')
print('原列表:', lst)
print(lst[::-1])
# start=7,stop 省略 step=-1
print(lst[7::-1])
# start=6,stop=0,step=-2
print(lst[6:0:-2])

a = 10  # 变量存储的是一个对象的引用
lst = [10, 20, 'python', 'hello']
print(10 in lst)  # True
print(100 in lst)  # False
print(10 not in lst)  # False
print(100 not in lst)  # True
print("id: ", id(lst))
print("type: ", type(lst))  # <class 'list'>
print("value: ", lst)
for item in lst:
    print(item)

'''列表生成式'''
print([i ** 2 for i in range(1, 10)])  # [1, 4, 9, 16, 25, 36, 49, 64, 81]
'''带守卫的列表生成式'''
print([i for i in range(1, 10) if bool(i % 2)])  # [1, 3, 5, 7, 9]

print('t' in 'python')  # True
print('w' not in 'python')  # True

'''list添加元素操作'''
# 向列表的末尾添加一个元素
lst = [10, 20, 30]
print('添加元素之前: ', lst, id(lst))
lst.append(100)
print('添加元素之后: ', lst, id(lst))
lst2 = ['hello', 'world']
lst.append(lst2)  # 将lst2做为一个元素添加到列表的末尾
# 向列表的末尾一次性添加多个元素
lst.extend(lst2)
print(lst)

# 在任意位置上添加一个元素
lst.insert(1, 90)
print(lst)

lst3 = [True, False, 'hello']
# 在任意的位置上添加N多个元素
lst[1:] = lst3
print(lst)

'''index方法'''
# 里面的两个参数为前闭后开[start, stop)
lst = ['hello', 'world', 98, 'hello']
print(lst.index('hello'))  # 如果列表中有相同元素只返回列表中相同元素的第一个元素的索引
# print(lst.index('Python'))  # ValueError: 'Python' is not in list
# print(lst.index('hello', 1, 3))  # ValueError: 'hello' is not in list   'world',98

print(lst.index('hello', 1, 4))  # 输出3

"""列表元素删除"""
lst = [10, 20, 30, 40, 50, 60, 30]
lst.remove(30)  # 从列表中移除一个元素，如果有重复元素只移第一个元素
print(lst)  # [10, 20, 40, 50, 60, 30]
# lst.remove(100) #ValueError: list.remove(x): x not in list

# pop()根据索引移除元素，pop方法会返回移除的元素
print(f"pop的元素为 {lst.pop(1)}")
print(lst)  # [10, 40, 50, 60, 30]
# lst.pop(5) #IndexError: pop index out of range  如果指定的索引位置不存在，将抛出异常
print(f"pop的元素为 {lst.pop()}")  # 如果不指定参数（索引），将删除列表中的最后一个元素
print(lst)  # [10, 40, 50, 60]

print('--------切片操作-删除至少一个元素，将产生一个新的列表对象---------')
new_list = lst[1:3]  # 操作区间为[1,3)
print('原列表: ', lst)  # [10, 40, 50, 60]
print('切片后的列表: ', new_list)  # [40, 50]

'''不产生新的列表对象，而是删除原列表中的内容'''
lst[1:3] = []
print(lst)  # [10, 60]

'''清除列表中的所有元素'''
lst.clear()
print(lst)  # []

'''del语句将列表对象删除'''
del lst
# print(lst)  # NameError: name 'lst' is not defined


"""列表元素修改"""
lst = [1, 2, 3, 4]
# 一次修改一个值
lst[2] = 100
print(lst)  # [1, 2, 100, 4]
lst[1:3] = [300, 400, 500, 600]  # 操作区间为[1,3)
print(lst)  # [1, 300, 400, 500, 600, 4]

'''sort'''
lst = [2, 5, 1, 3, 0, 4]
print('排序前的列表', lst, id(lst))
# 开始排序,调用列表对象的sort方法,默认升序排序
lst.sort()  # 直接改变原list中元素顺序，不产生新的list
print('排序后的列表', lst, id(lst))

# 通过指定关键字参数，将列表中的元素进行降序排序
lst.sort(reverse=True)  # reverse=True 表示降序排序, reverse=False就是升序排序
print('降序结果', lst)
lst.sort(reverse=False)
print('升序结果', lst)

print('-------使用内置函数sorted()对列表进行排序，将产生一个新的list对象-------------')
lst = [2, 5, 1, 3, 0, 4]
print('原列表', lst)
# 开始排序
new_list = sorted(lst)
print('原列表', lst)
print('排序产生的新列表', new_list)
# 指定关键字参数，实现列表元素的降序排序
desc_list = sorted(lst, reverse=True)
print(desc_list)

'''unpack'''
print("-------unpack------")
lst = [1, 2, 3]
a, b, c = lst
print(a, b, c)  # 1 2 3
lst = [1, 2, 3, 4]
a, b, *c = lst
print(a, b, c)  # 1 2 [3, 4]

# 遍历的同时获取每个元素的下标
print([(i, e) for i, e in enumerate(lst)])  # start默认从0开始
print([(i, e) for i, e in enumerate(lst, 1)])  # start指定从1开始
