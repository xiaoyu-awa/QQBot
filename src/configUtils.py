import yaml
import os

class YAMLConfigError(Exception):
    """自定义配置异常基类"""
    pass

class YAMLConfig:
    def __init__(self, file_path):
        """
        初始化YAML配置工具
        :param file_path: 配置文件路径
        """
        self.file_path = file_path
        self.data = {}
        self.load()

    def load(self):
        """
        加载配置文件
        :raises YAMLConfigError: 读取文件失败时抛出
        """
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self.data = yaml.safe_load(f) or {}
            else:
                self.data = {}
        except yaml.YAMLError as e:
            raise YAMLConfigError(f"YAML解析错误: {e}")
        except Exception as e:
            raise YAMLConfigError(f"文件读取失败: {e}")

    def save(self):
        """
        保存配置到文件
        :raises YAMLConfigError: 写入文件失败时抛出
        """
        try:
            # 自动创建不存在的目录
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

            with open(self.file_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(
                    self.data,
                    f,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False
                )
        except Exception as e:
            raise YAMLConfigError(f"文件保存失败: {e}")

    def get(self, key, default=None):
        """
        获取配置项
        :param key: 配置键，支持点分隔符（如：a.b.c）
        :param default: 默认值
        """
        keys = key.split('.')
        value = self.data
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key, value):
        """
        设置配置项
        :param key: 配置键，支持点分隔符（如：a.b.c）
        :param value: 配置值
        """
        keys = key.split('.')
        current = self.data
        for i, k in enumerate(keys[:-1]):
            if k not in current:
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value

config = YAMLConfig("config/config.yml")
sensitive_word = YAMLConfig("config/sensitive_word.yml")