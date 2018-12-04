"""
配置管理 管理站点配置文件的增删改查
"""
from typing import List
import os
from os import path

from common.Config import Config
from ProcessManager.Log import Log


class ConfigManager(Log):

    def __init__(self, config_dir: str, log_name: str):
        """ 配置管理类
        - config_dir str: 配置文件夹路径
        - log_name str: 要使用的log的名称
        """
        super().__init__("[CONFIG]", log_name)
        self.__config_dir = config_dir

        if path.isdir(self.__config_dir) is False:
            os.makedirs(self.__config_dir)

    def getConfig(self, cfg_id: str) -> Config:
        """ 获取指定配置 """
        if self.exists(cfg_id) is False:
            return None
        return Config.load(self.getConfigPath(cfg_id))

    def getConfigList(self) -> List[Config]:
        """ 获取所有有效配置 """
        ret = []
        for file in os.listdir(self.__config_dir):
            if not file.lower().endswith(".json"):
                continue
            cfg_id = file[:-5]
            config = self.getConfig(cfg_id)
            if config is not None and not config.check():
                ret.append(config)
        return ret

    def getConfigIdList(self) -> List[str]:
        """ 获取有效配置的ID列表 """
        return [i.id for i in self.getConfigList()]

    def getConfigPath(self, cfg_id: str) -> str:
        """ 获取指定配置的文件路径 """
        return path.join(self.__config_dir, "{}.json".format(cfg_id))

    def exists(self, cfg_id: str) -> bool:
        """ 返回指定配置时候已存在 """
        return path.isfile(self.getConfigPath(cfg_id))

    def add(self, config: Config) -> bool:
        """ 添加并保存配置
        - config Config: 要添加的配置
        - return bool: 返回添加是否成功
        """
        # 判断输入是否合法
        err = config.check()
        if err:
            self._warning("配置添加失败: 输入不合法, {}".format(err))
            return False

        # 判断是否已存在
        if self.exists(config.id):
            self._warning("配置添加失败: 已存在相同ID({})配置".format(config.id))
            return False

        # 尝试保存
        if config.save(self.getConfigPath(config.id)) is False:
            self._warning("配置添加失败: 配置文件保存失败, Config={}".format(config.toJSON()))
            return False

        self._info("配置添加成功(ID:{})".format(config.id))
        return True

    def remove(self, cfg_id: str) -> bool:
        """ 删除指定配置 """
        if self.exists(cfg_id) is False:
            self._warning("配置删除失败, 不存在ID为`{}`的配置".format(cfg_id))
            return True

        try:
            config = self.getConfig(cfg_id)
            os.remove(self.getConfigPath(cfg_id))
            self._info("配置删除成功, Config={}".format(config.toJSON()))
            return True
        except:
            self._warning("配置删除失败: 配置文件删除失败({})".format(cfg_id), exc_info=True)
            return False

    def update(self, config: Config, create=False) -> bool:
        """ 更新指定配置
        - config Config: 要更新的配置
        - create bool[False]: 如果不存在相同ID配置是否新增该配置
        - return bool: 返回更新是否成功
        """
        # 判断输入是否合法
        err = config.check()
        if err:
            self._warning("配置修改失败: 输入不合法, {}".format(err))
            return False

        # 判断配置是否存在
        if self.exists(config.id) is False:
            if create:
                return self.add(Config)
            else:
                self._warning("更新配置失败: 配置不存在(ID:{})".format(config.id))
                return False

        # 保存配置
        old_cfg = self.getConfig(config.id)
        if config.save(self.getConfigPath(config.id)) is False:
            self._warning("更新配置失败: 配置文件保存失败(ID:{})".format(config.id))
            return False

        self._info("更新配置成功, 旧配置Config={}".format(old_cfg.toJSON()))
        return True
