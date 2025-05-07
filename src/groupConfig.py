from enum import Enum
from typing import Dict, Any, Union

from src import configUtils
from src.configUtils import YAMLConfig


class ConfigItem(Enum):
    """配置项枚举（可扩展）"""
    RANDOMPIC = ("randomPic", "随机图片", bool)
    KEYWORD_MUTE = ("keyWordMute", "关键词屏蔽", bool)
    KEYWORDS = ("keyWords", "自定义关键词列表", list)

    def __init__(self, key: str, cn_name: str, value_type: type):
        self.key = key
        self.cn_name = cn_name
        self.value_type = value_type

    @classmethod
    def getConfigMap(cls) -> Dict[str, 'ConfigItem']:
        """获取配置键到枚举的映射"""
        return {item.key: item for item in cls}


class GroupConfig:
    # 配置项默认值和验证器
    CONFIG_SCHEMA = {
        ConfigItem.RANDOMPIC.key: {
            "default": False
        },
        ConfigItem.KEYWORD_MUTE.key: {
            "default": True
        },
        ConfigItem.KEYWORDS.key: {
            "default": []
        }
    }

    def __init__(self, yaml_config: YAMLConfig):
        self.config = yaml_config
        self.config_map = ConfigItem.getConfigMap()


    def getConfigItem(self, enum_item: ConfigItem) -> Dict[str, Any]:
        """获取配置项的元信息"""
        return {
            "key": enum_item.key,
            "cn_name": enum_item.cn_name,
            "type": enum_item.value_type,
            "default": self.CONFIG_SCHEMA[enum_item.key]["default"]
        }

    def listAllConfigItems(self) -> Dict[ConfigItem, Dict[str, Any]]:
        """列举所有可用配置项"""
        return {item: self.getConfigItem(item) for item in ConfigItem}

    def getConfigByEnum(self, group_id: Union[str, int], enum_item: ConfigItem) -> Any:
        """通过枚举获取配置项"""
        group_id = str(group_id)
        return self.config.get(group_id + "." + enum_item.key, None)

    def setConfigByEnum(self, group_id: Union[str, int], enum_item: ConfigItem, value: Any, auto_save: bool = True) -> None:
        """通过枚举设置配置项"""
        group_id = str(group_id)

        self.config.set(f"{group_id}.{enum_item.key}", value)
        if auto_save:
            self.config.save()

groupSettings = GroupConfig(configUtils.config)