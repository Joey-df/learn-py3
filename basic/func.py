def calc(a, b):  # a,b称为形式参数，简称形参,形参的位置是在函数的定义处
    c = a + b
    return c


def calc2(a: int, b: int) -> int:  # 明确给出参数类型和返回值类型
    return a + b


print(calc(10, 20))  # 10,20称为实际参数的值,简称 实参，实参的位置是函数的调用处
print(calc2(1, 2))
print(calc(b=10, a=20))  # =左侧的变量的名称称为  关键字参数

# 值传递与引用传递
print("值传递与引用传递:")
def fun1(arg1, arg2):
    print('arg1', arg1)  # 11
    print('arg2', arg2)  # [22, 33, 44]
    arg1 = 100  # 函数内部可以对所传实参的值进行修改（scala中是绝不允许的）
    arg2.append(10)
    print('arg1', arg1)  # 100
    print('arg2', arg2)  # [22, 33, 44, 10]
    # return # 无返回值return可以省略


n1 = 11
n2 = [22, 33, 44]
print('n1', n1)  # 11
print('n2', n2)  # [22, 33, 44]
fun1(n1, n2)  # 将位置传参,arg1,arg2，是函数定义处的形参，n1,n2是函数调用的处的实参，总结，实参名称与形参名称可以不一致

print('n1', n1)  # 11  不受影响
print('n2', n2)  # [22, 33, 44, 10]

'''在函数调用过程中，进行参数的传递
如果是不可变对象，在函数体的修改不会影响实参的值 arg1的修改为100，不会影响n1的值（实际上传递的是一个副本）
如果是可变对象，在函数体的的修改会影响到实参的值  arg2的修改，append(10)，会影响到n2的值
与Java一样
'''

'''
函数的返回值
 (1)如果函数没有返回值【函数执行完毕之后，不需要给调用处提供数据】 return可以省略不写
 (2)函数的返回值，如果是1个，直接返回类型
 (3)函数的返回值，如果是多个，返回的结果为元组
'''
print("函数的返回值:")
def fun2(num):
    odd = []  # 存奇数
    even = []  # 存偶数
    for i in num:
        if i % 2:
            odd.append(i)
        else:
            even.append(i)
    return odd, even  # 返回的是tuple


# 函数的调用
lst = [1, 2, 3, 4, 5, 6]
res = fun2(lst)
print(res)
odd, even = res
print(f"odd={odd}, even={even}")


# 默认值参数
print("默认值参数:")
def fun3(a, b=10):  # b称为默认值参数
    print(f'a={a}, b={b}')

# 函数的调用
fun3(100)
fun3(20, 30)
print('hello', end='\t')
print('world')

# 可变的位置参数
def fun4(*args):  # 函数定义时的 可变的位置参数
    print(args)
    # print(args[0])


fun4(10)  # (10,)
fun4(10, 30)  # (10, 30)
fun4(30, 405, 50)  # (30, 405, 50)


def func5(**args):  # 函数定义时的 可变的关键字参数
    print(args)


func5(a=10)  # {'a': 10}
func5(a=20, b=30, c=40)  # {'a': 20, 'b': 30, 'c': 40}

print('hello', 'world', 'Python')

'''
def fun6(*args,*args2):   
    pass   
    以上代码，程序会报错，个数可变的位置参数，只能是1个 
def fun6(**args,**args2):
    pass
    以上代码，程序会报错，个数可变的关键字参数，只能是1个 
'''

# 可变位置参数，可变关键字参数同时存在
def fun6(*args, **kwargs):
    pass

'''
def fun6(**args1,*arg2):
    pass
以上代码报错
在一个函数的定义过程中，既有个数可变的关键字形参，也有个数可变的位置形参，要求，个数可变的位置形参，放在个数可变的关键字形参之前
'''


def fun7(a, b, c):  # a,b,c在函数的定义处，所以是形式参数
    print(f'a={a}, b={b}, c={c}')


# 函数的调用
fun7(10, 20, 30)  # 函数调用时的参数传递，称为位置传参
lst = [11, 22, 33]
# 解包实参列表
print('-------将list或dict解包传参--------------')
fun7(*lst)  # 在函数调用时，将列表中的每个元素都转换为位置实参传入
fun7(a=100, c=300, b=200)  # 函数的调用，所以是关键字实参
kw = {'a': 111, 'b': 222, 'c': 333}
fun7(**kw)  # 在函数调用时，将字典中的键值对都转换为关键字实参传入


def f(a, b=10):  # b是在函数的定义处，所以b是形参，而且进行了赋值，所以b称为默认值形参
    print('a=', a)
    print('b=', b)


def f2(*args):  # 个数可变的位置形参
    print(args)


def f3(**args2):  # 个数可变的关键字形参
    print(args2)


f2(10, 20, 30, 40)
f3(a=11, b=22, c=33, d=44, e=55)


def f4(a, b, *, c, d):  # 从*之后的参数，在函数调用时，只能采用关键字参数传递
    print('a=', a)
    print('b=', b)
    print('c=', c)
    print('d=', d)


# 调用f4函数
# f4(10,20,30,40)  #位置实参传递
f4(a=10, b=20, c=30, d=40)  # 关键字实参传递
f4(10, 20, c=30, d=40)  # 前两个参数，采用的是位置实参传递，而c,d采用的是关键字实参传递
'''函数定义时的形参的顺序问题'''


def f6(*args, **kwargs):
    pass


def f7(a, b=10, *args, **kwargs):
    pass


def standard_arg(arg):
    pass


def pos_only_arg(arg, /):
    pass


def kwd_only_arg(*, arg):
    pass


def combined_example(pos_only_1, pos_only_2, /, pos_or_kwd_1, pos_or_kwd_2, *, kw_only_1, kw_only_2, **kwargs):
    pass

# 函数调用
combined_example(1, 2, 3, 1, kw_only_1=3, kw_only_2=4, a=5, b=6)
combined_example(1, 2, 3, pos_or_kwd_2=1, kw_only_1=3, kw_only_2=4, a=5, c=6)
combined_example(1, 2, pos_or_kwd_1=3, pos_or_kwd_2=1, kw_only_1=3, kw_only_2=4, a=5, w=6)

# 解包实参列表
print(list(range(3, 6)))  # normal call with separate arguments
args = [3, 6]
print(list(range(*args)))  # call with arguments unpacked from a list
print(list(range(*[3, 6])))


def fun8(a1, b1):
    c = a1 + b1  # c,就称为局部变量，因为c在是函数体内进行定义的变量,a,b为函数的形参，作用范围也是函数内部，相当于局部变量
    print(c)


# print(c1)  ,因为a1,c1超出了起作用的范围（超出了作用域）
# print(a1)

name = 'Jooen'  # name的作用范围为函数内部和外部都可以使用 -->称为全局变量
print(name)


def fun9():
    print(name)


# 调用函数
fun9()


def fun10():
    global age  # 函数内部定义的变量，局部变量，局部变量使用global声明，这个变量实际上就变成了全局变量
    age = 20
    print(f"函数内部age={age}")


fun10()
print(f"global 之后的 age={age}")


# 递归函数
# 求阶乘
def fac(n):
    if n == 1:
        return 1
    else:
        res = n * fac(n - 1)
        return res


print(fac(6))


# 求斐波那契数列的第n项
def fib(n):
    if n == 1:
        return 1
    elif n == 2:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


# 斐波那契数列第6位上的数字
print(fib(6))

print('------------------------------')
# 输出这个数列的前6位上的数字
for i in range(1, 7):
    print(f'第{i}项：{fib(i)}')

