import pytest
import os
from datetime import datetime

# 导入自定义夹具
pytest_plugins = ["core.fixtures"]

def pytest_configure(config):
    """配置pytest"""
    # 设置测试报告标题
    config.metadata["Project"] = "API Automation Test"
    config.metadata["Environment"] = os.getenv("TEST_ENV", "test")

def pytest_html_report_title(report):
    """设置HTML报告标题"""
    report.title = "API自动化测试报告"

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    """自定义测试报告"""
    # 这是pytest-html插件的钩子，可以用来增强报告内容
    pass
