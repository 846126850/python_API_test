import requests
from requests.exceptions import RequestException
import logging
from typing import Dict, Optional, Any, Tuple

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HttpClient:
    """HTTP请求客户端封装"""
    
    def __init__(self, base_url: str, timeout: int = 10, headers: Optional[Dict[str, str]] = None):
        """
        初始化HTTP客户端
        :param base_url: 基础URL
        :param timeout: 超时时间
        :param headers: 默认请求头
        """
        self.base_url = base_url
        self.timeout = timeout
        self.headers = headers or {}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def _handle_response(self, response: requests.Response) -> Tuple[Dict[str, Any], int]:
        """
        处理响应
        :param response: 响应对象
        :return: 响应体和状态码
        """
        try:
            response_data = response.json()
        except ValueError:
            response_data = {"text": response.text}
        
        logger.info(f"请求URL: {response.url}")
        logger.info(f"状态码: {response.status_code}")
        logger.info(f"响应内容: {response_data}")
        
        return response_data, response.status_code
    
    def get(self, url: str, params: Optional[Dict[str, Any]] = None, 
            headers: Optional[Dict[str, str]] = None) -> Tuple[Dict[str, Any], int]:
        """
        发送GET请求
        :param url: 接口路径
        :param params: 查询参数
        :param headers: 请求头
        :return: 响应体和状态码
        """
        full_url = f"{self.base_url}{url}"
        try:
            logger.info(f"发送GET请求: {full_url}, 参数: {params}")
            response = self.session.get(
                full_url,
                params=params,
                headers=headers,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except RequestException as e:
            logger.error(f"GET请求失败: {str(e)}")
            raise
    
    def post(self, url: str, data: Optional[Dict[str, Any]] = None, 
             json: Optional[Dict[str, Any]] = None, 
             headers: Optional[Dict[str, str]] = None) -> Tuple[Dict[str, Any], int]:
        """
        发送POST请求
        :param url: 接口路径
        :param data: 表单数据
        :param json: JSON数据
        :param headers: 请求头
        :return: 响应体和状态码
        """
        full_url = f"{self.base_url}{url}"
        try:
            logger.info(f"发送POST请求: {full_url}, 数据: {data or json}")
            response = self.session.post(
                full_url,
                data=data,
                json=json,
                headers=headers,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except RequestException as e:
            logger.error(f"POST请求失败: {str(e)}")
            raise
    
    def put(self, url: str, data: Optional[Dict[str, Any]] = None, 
            json: Optional[Dict[str, Any]] = None, 
            headers: Optional[Dict[str, str]] = None) -> Tuple[Dict[str, Any], int]:
        """发送PUT请求"""
        full_url = f"{self.base_url}{url}"
        try:
            logger.info(f"发送PUT请求: {full_url}, 数据: {data or json}")
            response = self.session.put(
                full_url,
                data=data,
                json=json,
                headers=headers,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except RequestException as e:
            logger.error(f"PUT请求失败: {str(e)}")
            raise
    
    def delete(self, url: str, params: Optional[Dict[str, Any]] = None, 
               headers: Optional[Dict[str, str]] = None) -> Tuple[Dict[str, Any], int]:
        """发送DELETE请求"""
        full_url = f"{self.base_url}{url}"
        try:
            logger.info(f"发送DELETE请求: {full_url}, 参数: {params}")
            response = self.session.delete(
                full_url,
                params=params,
                headers=headers,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except RequestException as e:
            logger.error(f"DELETE请求失败: {str(e)}")
            raise
    
    def close(self):
        """关闭会话"""
        self.session.close()
