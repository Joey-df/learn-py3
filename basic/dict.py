'''字典的创建方式'''
# key不允许重复
# value允许有重复
# key必须是不可变类型，如str,int,tuple，不可以是list/dict类型
'''使用{}创建字典'''
scores = {'张三': 100, '李四': 98, '王五': 45}
print(scores)
print(type(scores))

'''第二种创建dict()'''
student = dict(name='jack', age=20)
print(student)

'''空字典'''
d = {}
print(d)


'''获取字典的元素'''
scores = {'张三': 100, '李四': 98, '王五': 45}
'''第一种方式，使用[]'''
print(scores['张三'])
# print(scores['陈六']) #KeyError: '陈六'

'''第二种方式，使用get()方法'''
print(scores.get('张三'))
print(scores.get('陈六'))  # None
print(scores.get('麻七', 99))  # 99是在查找'麻七'所对的value不存在时，提供的一个默认值


'''key的判断'''
scores = {'张三': 100, '李四': 98, '王五': 45}
print('张三' in scores)
print('张三' not in scores)

del scores['张三']  # 删除指定的key-value对
# scores.clear()  #清空字典的元素
print(scores)
scores['陈六'] = 98  # 新增元素
print(scores)

scores['陈六'] = 100  # 修改元素
print(scores)

'''key-value操作'''
scores = {'张三': 100, '李四': 98, '王五': 45}
# 获取所有的key
keys = scores.keys()
print(keys)  # dict_keys(['张三', '李四', '王五'])
print(type(keys))  # <class 'dict_keys'>
print(list(keys))  # 将所有的key组成的视图转成列表
print("----遍历keys----")
for k in scores.keys():
    print(k, scores.get(k))

# 获取所有的value
values = scores.values()
print(values)  # dict_values([100, 98, 45])
print(type(values))  # <class 'dict_values'>
print(list(values))  # [100, 98, 45]
print("----遍历values----")
for v in scores.values():
    print(v)

# 获取所有的key-value对
items = scores.items()
print(items)  # dict_items([('张三', 100), ('李四', 98), ('王五', 45)])
print(list(items))  # [('张三', 100), ('李四', 98), ('王五', 45)] 转换之后的列表元素是由元组组成
print("----遍历key-value对----")
for k, v in scores.items():
    print(k, v)
print("----常规遍历方法----")
for key in scores:
    print(key, scores[key], scores.get(key))

'''字典生成式'''
items = ['Fruits', 'Books', 'Others']
prices = [96, 78, 85, 100, 120]
d = {item.upper(): price for item, price in zip(items, prices)}
print(d)
