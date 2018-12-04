from collections import Iterable
import re

import numpy as np

from SFE.Serialize import Serialize


class Config(Serialize):

    __regex_time = re.compile(r"^([01]\d|2[0-3]):([0-5]\d)$")

    def __init__(self):
        super().__init__()

        self.id = None
        self.name = None
        self.upload_func = None
        self.video_source = None
        self.Ringelmann = None
        self.save_path = None
        self.border = None
        self.start_time = None
        self.stop_time = None

    def check(self) -> str:
        # id
        if not (isinstance(self.id, str) and self.id):
            return "id不能为空且类型必须为字符串"
        # save_path
        if not (isinstance(self.save_path, str) and self.save_path):
            return "save_path不能为空且类型必须为字符串"
        # border
        if self.border is not None:
            try:
                if not isinstance(self.border, Iterable):
                    raise Exception()
                border = np.array(self.border, dtype=float)
                if (
                    border.ndim != 3 or
                    not (border.shape[0] == border.shape[2] == 2) or
                    border.shape[1] < 2 or
                    not (np.all(border >= 0) and np.all(border <= 100))
                ):
                    raise Exception()
            except:
                return "当车道边界不为空时, 车道上下边界数组长度必须相等, 且每个成员必须为数值型数组、每个成员的数组长度必须为2"
        # Ringelmann
        if not (isinstance(self.Ringelmann, int) and 0 <= self.Ringelmann <= 5):
            return "林格曼阈值必须为整数, 且值在0到5之间"
        # 时间
        for time in (self.start_time, self.stop_time):
            if time is None:
                continue
            if not (isinstance(time, str) and self.__regex_time.match(time) is not None):
                return '时间必须为字符串, 且格式必须为"HH:mm", 长度不足两位时需要补0'
        return ""
