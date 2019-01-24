from SystemSetting import SystemData as SD

# 调度表
class Schedulsheet(SD):
    def __init__(self,name: str):
        self.name =name
        
    
    property
    def savedata(self):
        import pickle
        # 保存调度表
        with open('Schedul.bin','wb') as f:
            pickle.dump(self.data,f)

class PeopleSchedul:
    """
        @ 人员调度
    """

    def __init__(self,people: str,sites: list):
        pass

