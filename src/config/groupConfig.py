from enum import Enum
from typing import Dict, Any

from .configUtils import YAMLConfig


class GroupConfigItem(Enum):
    """配置项枚举（可扩展）"""
    RANDOMPIC = ("randomPic", "随机图片", bool)
    KEYWORD_MUTE = ("keyWordMute", "关键词屏蔽", bool)
    KEYWORDS = ("keyWords", "自定义关键词列表", list)

    def __init__(self, key: str, cn_name: str, value_type: type):
        self.key = key
        self.cn_name = cn_name
        self.value_type = value_type

    @classmethod
    def getConfigMap(cls) -> Dict[str, 'GroupConfigItem']:
        """获取配置键到枚举的映射"""
        return {item.key: item for item in cls}


class GroupConfig:
    # 配置项默认值和验证器
    CONFIG_SCHEMA = {
        GroupConfigItem.RANDOMPIC.key: {
            "default": False
        },
        GroupConfigItem.KEYWORD_MUTE.key: {
            "default": True
        },
        GroupConfigItem.KEYWORDS.key: {
            "default": []
        }
    }

    def __init__(self, group_id : str):
        self.config = YAMLConfig('config/config.yml')
        self.config_map = GroupConfigItem.getConfigMap()
        self.group_id = str(group_id)


    def getConfigItem(self, enum_item: GroupConfigItem) -> Dict[str, Any]:
        """获取配置项的元信息"""
        return {
            "key": enum_item.key,
            "cn_name": enum_item.cn_name,
            "type": enum_item.value_type,
            "default": self.CONFIG_SCHEMA[enum_item.key]["default"]
        }

    def listAllConfigItems(self) -> Dict[GroupConfigItem, Dict[str, Any]]:
        """列举所有可用配置项"""
        return {item: self.getConfigItem(item) for item in GroupConfigItem}

    def getConfigByEnum(self, enum_item: GroupConfigItem) -> Any:
        """通过枚举获取配置项"""
        group_id = str(self.group_id)
        var = self.config.get(self.group_id + "." + enum_item.key, None)
        if var is None:
            self.config.set(f"{self.group_id}.{enum_item.key}", self.CONFIG_SCHEMA[enum_item.key]["default"])
        return self.config.get(f"{self.group_id}.{enum_item.key}")

    def setConfigByEnum(self, enum_item: GroupConfigItem, value: Any, auto_save: bool = True) -> None:
        """通过枚举设置配置项"""
        group_id = str(self.group_id)

        self.config.set(f"{self.group_id}.{enum_item.key}", value)
        if auto_save:
            self.config.save()