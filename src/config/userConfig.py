from enum import Enum
from typing import Dict, Any, Union

from .configUtils import YAMLConfig


class UserConfigItem(Enum):
    """配置项枚举（可扩展）"""
    SIGNINTIME = ("signInTime", "上一次签到时间", int)

    def __init__(self, key: str, cn_name: str, value_type: type):
        self.key = key
        self.cn_name = cn_name
        self.value_type = value_type

    @classmethod
    def getConfigMap(cls) -> Dict[str, 'UserConfigItem']:
        """获取配置键到枚举的映射"""
        return {item.key: item for item in cls}


class UserConfig:
    # 配置项默认值和验证器
    CONFIG_SCHEMA = {
        UserConfigItem.SIGNINTIME.key: {
            "default": 0
        }
    }

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.config_map = UserConfigItem.getConfigMap()
        self.config = YAMLConfig('config/userConfig.yml')

    def getConfigItem(self, enum_item: UserConfigItem) -> Dict[str, Any]:
        """获取配置项的元信息"""
        return {
            "key": enum_item.key,
            "cn_name": enum_item.cn_name,
            "type": enum_item.value_type,
            "default": self.CONFIG_SCHEMA[enum_item.key]["default"]
        }

    def listAllConfigItems(self) -> Dict[UserConfigItem, Dict[str, Any]]:
        """列举所有可用配置项"""
        return {item: self.getConfigItem(item) for item in UserConfigItem}

    def getConfigByEnum(self, enum_item: UserConfigItem) -> Any:
        """通过枚举获取配置项"""
        group_id = str(self.user_id)
        var = self.config.get(self.user_id + "." + enum_item.key, None)
        if var is None:
            self.config.set(f"{self.user_id}.{enum_item.key}", self.CONFIG_SCHEMA[enum_item.key]["default"])
        return self.config.get(f"{self.user_id}.{enum_item.key}")

    def setConfigByEnum(self, enum_item: UserConfigItem, value: Any, auto_save: bool = True) -> None:
        """通过枚举设置配置项"""
        group_id = str(self.user_id)

        self.config.set(f"{self.user_id}.{enum_item.key}", value)
        if auto_save:
            self.config.save()

    def initConfig(self):
        for key, value in self.CONFIG_SCHEMA.items():
            self.config.set(f"{self.user_id}.{key}", value["default"])
            self.config.save()
