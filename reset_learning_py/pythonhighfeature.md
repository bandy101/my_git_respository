
-------python高级特性----------


#判断一个对象是否可迭代：
    from collections import Iterable(迭代器)
    isinstance('abc', Iterable) # 判断str是否可迭代    ###-----True

#生成器（generate)：  
    如果列表元素可以按照某种算法推算出来，那我们是否可以在循环的过程中不断推算出后续的元素呢？这样就不必创建完整的list，从而节省大量的空间。在Python中，这种一边循环一边计算的机制，称为生成器：generator。

    ways-1:把一个列表生成式的[]改成()
        '''      g = (x * x for x in range(10))  ''' 
        <generator object <genexpr> at 0x1022ef630>
        next(g),就计算出g的下一个元素的值，直到计算到最后一个元素，没有更多的元素时，抛出StopIteration的错误。
        or:  for n in g:
                 print(n)
    ways-2:定义函数算法推出后面结果值
        def fib(max):
        n, a, b = 0, 0, 1
        while n < max: 
            print(b)      #将print 改成yield b   become-->genarator
            a, b = b, a + b
            n = n + 1
        return 'done'               ##可以从第一个元素开始，推算出后续任意的元素
        基本不使用next 常用循环：
            for n in fib(6):
                print(n)

#序列是可Iterable，不是Iterator  (list,dict,str,set,tulple)->迭代器 ：iter(序列(Iterable)) 
from functools import reduce 
    f():
        return x?y  #递归
    reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)
    >> from functools import reduce
***    --reduce 经典    
example1:
>>> def fn(x, y):
...     return x * 10 + y
...
>>> reduce(fn, [1, 3, 5, 7, 9])
13579
example2:
#from functools import reduce
DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
def str2int(s):
    def fn(x, y):
        return x * 10 + y
    def char2num(s):
        return DIGITS[s]
    return reduce(fn, map(char2num, s))
***
#列表生成式：
    [x * x for x in range(1, 11) if x % 2 == 0]			[4, 16, 36, 64, 100]
    [m + n for m in 'ABC' for n in 'XYZ']  #两层循环迭代
    ['AX', 'AY', 'AZ', 'BX', 'BY', 'BZ', 'CX', 'CY', 'CZ']
    # 简化
        d = {'x': 'A', 'y': 'B', 'z': 'C' }
        [k + '=' + v for k, v in d.items()]
        ['y=B', 'x=A', 'z=C']

#内建函数
    filter()也接收一个函数和一个序列。和map()不同的是，filter()把传入的函数依次作用于每个元素，然后根据返回值是True还是False决定保留还是丢弃该元素。
        def is_odd(n):
            return n % 2 == 1
        list(filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15]))
        # 结果: [1, 5, 9, 15]
    sorted()函数也是一个高阶函数，它还可以接收一个key函数来实现自定义的排序，例如按绝对值大小排序：
    key指定的函数将作用于list的每一个元素上，并根据key函数返回的结果进行排序。对比原始的list和经过key=abs处理过的list
        sorted([36, 5, -12, 9, -21], key=abs)
        [5, 9, -12, -21, 36]
        要进行反向排序，不必改动key函数，可以传入第三个参数reverse=True：
        sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower, reverse=True)
        ['Zoo', 'Credit', 'bob', 'about']

#闭包
    相关参数和变量都保存在返回的函数中，这种称为“闭包“ [返回函数]
    def count():
    fs = []
    for i in range(1, 4):
        def f():
             return i*i
        fs.append(f)
    return fs
    f1, f2, f3 = count()
    全部都是9！原因就在于返回的函数引用了变量i，但它并非立刻执行。等到3个函数都返回时，它们所引用的变量i已经变成了3，因此最终结果为9。
    返回闭包时牢记一点：返回函数不要引用任何循环变量，或者后续会发生变化的变量。 

#装饰器 
    log()是一个decorator，返回一个函数，所以，原来的now()函数仍然存在，只是现在同名的now变量指向了新的函数，
    于是调用now()将执行新函数，即在log()函数中返回的wrapper()函数。
#wrapper()函数的参数定义是(*args, **kw)，因此，wrapper()函数可以接受任意参数的调用。
    在wrapper()函数内，首先打印日志，再紧接着调用原始函数。
    def log(func):
        def wrapper(*args, **kw):
            print('call %s():' % func.__name__)
            return func(*args, **kw)
        return wrapper
    @log
    def now():
        print('2015-3-25')
    相当于 log(now)  >>> now()
        call now():
        2015-3-25
因为返回的那个wrapper()函数名字就是'wrapper'，所以，需要把原始函数的__name__等属性复制到wrapper()函数中，否则，有些依赖函数签名的代码执行就会出错。
不需要编写wrapper.__name__ = func.__name__这样的代码，Python内置的functools.wraps就是干这个事的，所以，一个完整的decorator的写法如下：
    import functools
    def log(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('call %s():' % func.__name__)
            return func(*args, **kw)
        return wrapper
    if decorator need a args:
        def log(text):
            def decorator(func):
                import functools
                @functools.wrap(func)
                def wrapper(*args,**k):
                    print()
                    return func(*args,**k)
                return  wrapper
            return decorator
            callable(func_name) ##查看参数是否可调用

#偏函数
    调用 functools.partial
    example:
        int2 = functools.partial(int,base=2)## int2('10000',2)=16
        int2('10010') 创建偏函数时，实际上可以接收函数对象、*args和**kw这3个参数，当传入：相当如下：
            kw = { 'base': 2 }
            int('10000', **kw)

#类
    ~访问限制：
        class A():
            def __init__():
                self.__xx=xx   ##__私有变量 外部范围通过inistance._A__xx 访问

        _name，这样的实例变量外部是可以访问的，但是，按照约定俗成的规定，当你看到这样的变量时，意思就是，“虽然我可以被访问，但是，请把我视为私有变量，不要随意访问”。
    
    ~多态：
        当我们定义一个class的时候，我们实际上就定义了一种数据类型。我们定义的数据类型和Python自带的数据类型，比如str、list、dict没什么两样：
            判断一个变量是否是某个类型可以用isinstance()判断：
                a = list() # a是list类型            
                b = Animal() # b是Animal类型
                c = Dog() # c是Dog类型
                >>> isinstance(a, list)True         >>> isinstance(b, Animal)     True  >>> isinstance(c, Dog) True
        在继承关系中，如果一个实例的数据类型是某个子类，那它的数据类型也可以被看做是父类。但是，反过来就不行!
    ~获取对象信息：
        判断一个对象是否是函数怎么办？可以使用types模块中定义的常量：                 or:callable(object_name)
            import types
                >>> def fn():
...                 pass
...
        >>> type(fn)==types.FunctionType    True
        >>> type(abs)==types.BuiltinFunctionType    True        #内建函数
        >>> type(lambda x: x)==types.LambdaType True 
        >>> type((x for x in range(10)))==types.GeneratorType   True   
    对于继承关系一般使用 isintance(,)而少使用type() 并且还可以判断一个变量是否是某些类型中的一种，比如下面的代码就可以判断是否是list或者tuple：
        >>> isinstance([1, 2, 3], (list, tuple))    True
        >>> isinstance((1, 2, 3), (list, tuple))    True    

    如果要获得一个对象的所有属性和方法，可以使用dir()函数，它返回一个包含字符串的list，比如，获得一个str对象的所有属性和方法：
    >>> dir('ABC')
    ['__add__', '__class__',..., '__subclasshook__', 'capitalize', 'casefold',..., 'zfill']

    类似__xxx__的属性和方法在Python中都是有特殊用途的，比如__len__方法返回长度。在Python中，如果你调用len()函数试图获取一个对象的长度，实际上，在len()函数内部，它自动去调用该对象的__len__()方法，所以，下面的代码是等价的：
        >>> len('ABC')  3
        >>> 'ABC'.__len__()3
    配合getattr()、setattr()以及hasattr()，我们可以直接操作一个对象的状态：
        >>> getattr(obj, 'z', 404) # 获取属性'z'，如果不存在，返回默认值404

##面向对象编程高级特性:
    class A():
        pass
    给类绑定方法：
    def p():
        pass
    A.p=p (A类永久增加p方法)
    如果我们想要限制实例的属性怎么办？比如，只允许对Student实例添加name和age属性。
        为了达到限制的目的，Python允许在定义class的时候，定义一个特殊的__slots__变量，来限制该class实例能添加的属性：
        class A():
        __slot__=('name','age')
        pass
        a = A()   a.name = xx  a.score##错误 slot中不包含score
    
#property
    Python内置的@property装饰器就是负责把一个方法变成属性调用
    @property的实现比较复杂，我们先考察如何使用。把一个getter方法变成属性，只需要加上@property就可以了，
    此时，@property本身又创建了另一个装饰器@score.setter，负责把一个setter方法变成属性赋值，于是，我们就拥有一个可控的属性操作：
        class Student(object):
            @property
            def score(self):
                return self._score
            @score.setter
            def score(self, value):
                if not isinstance(value, int):
                    raise ValueError('score must be an integer!')
                if value < 0 or value > 100:
                    raise ValueError('score must between 0 ~ 100!')
                self._score = value
        >>> s = Student()
        >>> s.score = 60 # OK，实际转化为s.set_score(60)
        >>> s.score # OK，实际转化为s.get_score()   60
#多重继承   MixIn
    在设计类的继承关系时，通常，主线都是单一继承下来的，例如，Ostrich(鸵鸟)继承自Bird。但是，如果需要“混入”额外的功能，通过多重继承就可以实现，比如，让Ostrich除了继承自Bird外，再同时继承Runnable。这种设计通常称之为MixIn。
    MixIn的目的就是给一个类增加多个功能，这样，在设计类的时候，我们优先考虑通过多重继承来组合多个MixIn的功能，而不是设计多层次的复杂的继承关系。
    Python自带的很多库也使用了MixIn。举个例子，Python自带了TCPServer和UDPServer这两类网络服务，而要同时服务多个用户就必须使用多进程或多线程模型，这两种模型由ForkingMixIn和ThreadingMixIn提供。通过组合，我们就可以创造出合适的服务来。
#定制类
    __len__()方法是为了能让class作用于len()函数。
    __str__()作用于print
    >>> s = Student('Michael')
    >>> s       <__main__.Student object at 0x109afb310>
    直接显示变量作用的不是__str__()而是 __repr__()
    class Student(object):
        def __init__(self, name):
            self.name = name
        def __str__(self):
            return 'Student object (name=%s)' % self.name
        __repr__ = __str__
    __iter__:
        如果一个类想被用于for ... in循环，类似list或tuple那样，就必须实现一个__iter__()方法，该方法返回一个迭代对象，然后，Python的for循环就会不断调用该迭代对象的__next__()方法拿到循环的下一个值，直到遇到StopIteration错误时退出循环。
        class Fib(object):
            def __init__(self):
                self.a, self.b = 0, 1 # 初始化两个计数器a，b

            def __iter__(self):
                return self # 实例本身就是迭代对象，故返回自己

            def __next__(self):
                self.a, self.b = self.b, self.a + self.b # 计算下一个值
                if self.a > 100000: # 退出循环的条件
                    raise StopIteration()
                return self.a # 返回下一个值
        >>> for n in Fib(): ####斐波那契数列
                print(n)
        __getitem__:
            Fib实例虽然能作用于for循环，看起来和list有点像，但是，把它当成list来使用还是不行，比如，取第5个元素：Fib()[4]
                要表现得像list那样按照下标取出元素，需要实现__getitem__()方法：
            class Fib(object):
                def __getitem__(self, n):
                    a, b = 1, 1
                    for x in range(n):
                        a, b = b, a + b
                    return a
            如果 Fib()[:] 使用切片 则报错
                if isinstance(n, slice): # n是切片
                    start = n.start
                    stop = n.stop
                    if start is None:
                        start = 0
                    a, b = 1, 1
                    L = []
                    for x in range(stop):
                        if x >= start:
                            L.append(a)
                        a, b = b, a + b
                    return L
            要正确实现一个__getitem__()还是有很多工作要做的。
            此外，如果把对象看成dict，__getitem__()的参数也可能是一个可以作key的object，例如str。
            与之对应的是__setitem__()方法，把对象视作list或dict来对集合赋值。最后，还有一个__delitem__()方法，用于删除某个元素。
#__getattr__:
    在没有找到属性的情况下，才调用__getattr__：
    class Student(object):
        def __getattr__(self, attr):
            if attr=='age':
                return lambda: 25
__call__:
    一个对象实例可以有自己的属性和方法，当我们调用实例方法时，我们用instance.method()来调用。能不能直接在实例本身上调用呢？在Python中，答案是肯定的。
    任何类，只需要定义一个__call__()方法，就可以直接对实例进行调用。请看示例：
    class Student(object):
        def __init__(self, name):
            self.name = name
        def __call__(self):
            print('My name is %s'%self.name)
    >>> s = Student('Michael')
    >>> s() # self参数不要传入
    My name is Michael.

#枚举类
    JAN = 1
    FEB = 2
    MAR = 3
    ...
    NOV = 11
    DEC = 12
    from enum import Enum
    Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
    value属性则是自动赋给成员的int常量，默认从1开始计数
    Month.Jan.value =1
#元类 metaclass
    h = Hello()
    type()函数可以查看一个类型或变量的类型，Hello是一个class，它的类型就是type，而h是一个实例，它的类型就是class Hello。
    >>> print(type(Hello))  <class 'type'>
    >>> print(type(h))      <class 'Hello'>
#type()函数既可以返回一个对象的类型，又可以创建出新的类型，比如，我们可以通过type()函数创建出Hello类，而无需通过class Hello(object)...的定义：
         def fn(self, name='world'):    print('Hello, %s.' % name)
    Hello = type('Hello', (object,), dict(hello=fn)) # 创建Hello class
    要创建一个class对象，type()函数依次传入3个参数：
    class的名称；
    继承的父类集合，注意Python支持多重继承，如果只有一个父类，别忘了tuple的单元素写法；
    class的方法名称与函数绑定，这里我们把函数fn绑定到方法名hello上。
#通过type()函数创建的类和直接写class是完全一样的，因为Python解释器遇到class定义时，仅仅是扫描一下class定义的语法，然后调用type()函数创建出class。
    # metaclass是类的模板，所以必须从`type`类型派生：
    class ListMetaclass(type):
        def __new__(cls, name, bases, attrs):
            attrs['add'] = lambda self, value: self.append(value)
            return type.__new__(cls, name, bases, attrs)
    class MyList(list, metaclass=ListMetaclass):    
        pass
传入关键字参数metaclass时，魔术就生效了，它指示Python解释器在创建MyList时，要通过ListMetaclass.__new__()来创建，在此，我们可以修改类的定义，比如，加上新的方法，然后，返回修改后的定义。

__new__()方法接收到的参数依次是：
    当前准备创建的类的对象；
    类的名字；
    类继承的父类集合；
    类的方法集合。atrrs  集合.items()
#ORM全称“Object Relational Mapping”，即对象-关系映射，就是把关系数据库的一行映射为一个对象，也就是一个类对应一个表
这样，写代码更简单，不用直接操作SQL语句。要编写一个ORM框架，所有的类都只能动态定义，因为只有使用者才能根据表的结构定义出对应的类来。




