import pytest
import json
from typing import Dict, Any

# 测试数据 - 可以放在单独的data目录下
TEST_DATA = {
    "get_user": [
        (1, 200, "John Doe"),    # 用户ID, 预期状态码, 预期姓名
        (999, 404, None)        # 不存在的用户
    ],
    "create_user": [
        ({"name": "New User", "email": "new@example.com"}, 201),  # 有效数据
        ({"name": "", "email": "invalid"}, 400)                   # 无效数据
    ]
}

class TestUserAPI:
    """用户相关接口测试"""
    
    def test_get_user_list(self, http_client):
        """测试获取用户列表"""
        response, status_code = http_client.get("/users")
        
        # 断言状态码
        assert status_code == 200, f"预期状态码200，实际得到{status_code}"
        
        # 断言响应结构
        assert isinstance(response, dict), "响应应该是一个字典"
        assert "data" in response, "响应中缺少data字段"
        assert isinstance(response["data"], list), "data应该是一个列表"
    
    @pytest.mark.parametrize("user_id, expected_status, expected_name", TEST_DATA["get_user"])
    def test_get_user_detail(self, http_client, user_id, expected_status, expected_name):
        """测试获取用户详情"""
        response, status_code = http_client.get(f"/users/{user_id}")
        
        # 断言状态码
        assert status_code == expected_status, \
            f"用户ID {user_id}: 预期状态码{expected_status}，实际得到{status_code}"
        
        # 如果预期成功，检查更多字段
        if expected_status == 200:
            assert "name" in response, "响应中缺少name字段"
            assert response["name"] == expected_name, \
                f"预期姓名{expected_name}，实际得到{response['name']}"
    
    @pytest.mark.parametrize("user_data, expected_status", TEST_DATA["create_user"])
    def test_create_user(self, http_client, auth_headers, user_data, expected_status):
        """测试创建用户"""
        response, status_code = http_client.post(
            "/users",
            json=user_data,
            headers=auth_headers
        )
        
        # 断言状态码
        assert status_code == expected_status, \
            f"创建用户: 预期状态码{expected_status}，实际得到{status_code}"
        
        # 如果创建成功，验证返回的数据
        if expected_status == 201:
            assert "id" in response, "创建用户成功但响应中没有id"
            assert response["name"] == user_data["name"], "创建的用户名不匹配"
