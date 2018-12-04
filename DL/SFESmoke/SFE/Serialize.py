import json


class Serialize:
    """ 这个对象为子类添加了四个方法 分别是:
    - toDict 实例方法: 返回子类的 `__dict__` 属性
    - fromDict 类方法: 从字典数据中生成并返回子类对象, 与`toDict`方法对应
    - save 实例方法: 调用`toDict`方法并将生成的`dict`以json格式保存到指定文件中
    - load 类方法: 从json格式的文件中生成并返回子类对象, 与`save`方法对应
    """

    def toDict(self):
        return self.__dict__

    @classmethod
    def fromDict(cls, data: dict):
        result = cls()
        result_dict = result.toDict()
        for k in result_dict:
            result_dict[k] = data.get(k, result_dict[k])
        return result

    def toJSON(self):
        return json.dumps(self.toDict(), ensure_ascii=False, indent=4)

    @classmethod
    def fromJSON(cls, data: str):
        data = json.loads(data)
        return cls.fromDict(data)

    def save(self, save_path) -> bool:
        with open(save_path, "w", encoding="utf-8") as fp:
            try:
                json.dump(self.toDict(), fp, ensure_ascii=False, indent=4)
                return True
            except:
                return False

    @classmethod
    def load(cls, save_path):
        with open(save_path, encoding="utf-8") as fp:
            try:
                data = json.load(fp)
                return cls.fromDict(data)
            except:
                return cls()
