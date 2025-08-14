import yaml
import os
from typing import Dict, Any, Optional

class Config:
    """配置管理类"""
    
    def __init__(self, config_file: str = "config/config.yaml"):
        """
        初始化配置
        :param config_file: 配置文件路径
        """
        self.config_file = config_file
        self.config = self._load_config()
        self.environment = os.getenv("TEST_ENV", self.config.get("default_env", "test"))
    
    def _load_config(self) -> Dict[str, Any]:
        """
        加载配置文件
        :return: 配置字典
        """
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            raise Exception(f"配置文件 {self.config_file} 不存在")
        except yaml.YAMLError as e:
            raise Exception(f"解析配置文件出错: {str(e)}")
    
    def get_env_config(self, env: Optional[str] = None) -> Dict[str, Any]:
        """
        获取指定环境的配置
        :param env: 环境名称
        :return: 环境配置字典
        """
        env = env or self.environment
        env_config = self.config.get("environments", {}).get(env)
        if not env_config:
            raise Exception(f"未找到环境 {env} 的配置")
        return env_config
    
    def get_base_url(self, env: Optional[str] = None) -> str:
        """获取基础URL"""
        return self.get_env_config(env).get("base_url", "")
    
    def get_timeout(self, env: Optional[str] = None) -> int:
        """获取超时时间"""
        return self.get_env_config(env).get("timeout", 10)
    
    def get_headers(self, env: Optional[str] = None) -> Dict[str, str]:
        """获取请求头"""
        return self.get_env_config(env).get("headers", {})
