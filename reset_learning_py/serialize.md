#在程序运行的过程中，所有的变量都是在内存中

#一旦程序结束，变量所占用的内存就被操作系统全部回收。

#序列化  在Python中叫pickling，在其他语言中也被称之为serialization，marshalling，flattening等等，都是一个意思。
    我们把变量从内存中变成可存储或传输的过程称之为序列化
#反序列化
    把变量内容从序列化的对象重新读到内存里称之为反序列化，即unpickling。

>>>let's coding
    import pickle
    pickle.dumps()方法把任意对象序列化成一个bytes，然后，就可以把这个bytes写入文件。
    或者用另一个方法pickle.dump()直接把对象序列化后写入一个file-like Object::~像open()函数返回的这种有个read()方法的对象，在Python中统称为file-like Object。
>>> d = dict(name='Bob', age=20, score=88)
>>> pickle.dumps(d)
b'\x80\x03}q\x00(X\x03\x00\x00\x00ageq\x01K\x14X\x05\x00\x00\x00scoreq\x02KXX\x04\x00\x00\x00nameq\x03X\x03\x00\x00\x00Bobq\x04u.'
>>> f = open('dump.txt', 'wb')
>>> pickle.dump(d, f)
>>> f.close()
#把对象从磁盘读到内存时，可以先把内容读到一个bytes，然后用pickle.loads()方法反序列化出对象，也可以直接用pickle.load()方法从一个file-like Object中直接反序列化出对象。
>>> f = open('dump.txt', 'rb')
>>> d = pickle.load(f)
>>> f.close()
>>> d
{'age': 20, 'score': 88, 'name': 'Bob'}

#JSON
    要在不同的编程语言之间传递对象，就必须把对象序列化为标准格式，比如XML，但更好的方法是序列化为JSON，
    因为JSON表示出来就是一个字符串，可以被所有语言读取，也可以方便地存储到磁盘或者通过网络传输。
    JSON不仅是标准格式，并且比XML更快，而且可以直接在Web页面中读取，非常方便。
    JSON类型 	Python类型
    {} 	        dict
    [] 	        list
    "string" 	str
    1234.56 	int或float
    true/false 	True/False
    null 	    None
#Python对象到JSON格式的转换
>>> import json

>>> d = dict(name='Bob', age=20, score=88)
>>> json.dumps(d)
'{"age": 20, "score": 88, "name": "Bob"}'
#dumps()方法返回一个str，内容就是标准的JSON。类似的，dump()方法可以直接把JSON写入一个file-like Object。

#把JSON反序列化为Python对象，用loads()或者对应的load()方法，前者把JSON的字符串反序列化，后者从file-like Object中读取字符串并反序列化：
>>> json_str = '{"age": 20, "score": 88, "name": "Bob"}'
>>> json.loads(json_str)
{'age': 20, 'score': 88, 'name': 'Bob'}
    可选参数default就是把任意一个对象变成一个可序列为JSON的对象，
    def student2dict(std):
        return {
            'name': std.name,
            'age': std.age,
            'score': std.score
        }
    s = Student('Bob', 20, 88) 
>>>print(json.dumps(s, default=student2dict))
{"age": 20, "name": "Bob", "score": 88}
#这样，Student实例首先被student2dict()函数转换成dict，然后再被顺利序列化为JSON：|>

#class的实例都有一个__dict__属性，它就是一个dict，用来存储实例变量。也有少数例外，比如定义了__slots__(限制函数外部设置新的变量)的class。
print(json.dumps(s, default=lambda obj: obj.__dict__))

###如果我们要把JSON反序列化为一个Student对象实例，json.loads()方法首先转换出一个dict对象,
#然后，我们传入的object_hook函数负责把dict转换为Student实例：
    def dict2student(d):
        return Student(d['name'], d['age'], d['score'])
>>> json_str = '{"age": 20, "score": 88, "name": "Bob"}'
>>> print(json.loads(json_str, object_hook=dict2student))
<__main__.Student object at 0x10cd3c190>