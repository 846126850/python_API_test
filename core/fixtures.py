import pytest
from core.config import Config
from core.http_client import HttpClient

@pytest.fixture(scope="session")
def config():
    """全局配置夹具"""
    return Config()

@pytest.fixture(scope="session")
def http_client(config):
    """HTTP客户端夹具"""
    client = HttpClient(
        base_url=config.get_base_url(),
        timeout=config.get_timeout(),
        headers=config.get_headers()
    )
    yield client
    client.close()

@pytest.fixture(scope="function")
def auth_headers(http_client):
    """获取认证头的夹具（示例）"""
    # 实际项目中这里应该调用登录接口获取token
    # 这里只是示例
    token = "test_token"
    return {"Authorization": f"Bearer {token}"}
