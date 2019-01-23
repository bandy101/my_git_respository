

# 系统设置
class SystemData:
    '''
        @ 数据路径
        @ 权限
        @ 人员记录表
    '''
    
    def __init__(self,name: str,permission: bool,address: str):
        
        self.name = name # 人员
        self.permission = permission # 访问数据保存文件夹的权限
        self.address = address # 数据保存目录

    @property
    def data(self):
        return self.__dict__
    
    @property
    def savedata(self):
        import pickle
        
        # 保存人员记录表
        with open('people.bin','wb') as f:
            pickle.dump(self.data,f)