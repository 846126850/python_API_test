import os
import pytest
import argparse
from datetime import datetime

def run_tests():
    """运行测试的主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="运行API自动化测试")
    parser.add_argument("--env", help="指定测试环境 (dev/test/prod)", default="test")
    parser.add_argument("--report", help="指定报告目录", default="reports")
    parser.add_argument("--allure", help="指定allure结果目录", default="allure-results")
    parser.add_argument("--marker", help="指定要运行的测试标记", default="")
    parser.add_argument("--testcase", help="指定要运行的测试用例或目录", default="tests")
    
    args = parser.parse_args()
    
    # 设置环境变量
    os.environ["TEST_ENV"] = args.env
    
    # 创建报告目录
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = os.path.join(args.report, timestamp)
    os.makedirs(report_dir, exist_ok=True)
    
    # 构建pytest命令参数
    pytest_args = [
        args.testcase,
        f"--html={os.path.join(report_dir, 'report.html')}",
        f"--self-contained-html",
        f"--alluredir={args.allure}"
    ]
    
    # 如果指定了测试标记，添加标记参数
    if args.marker:
        pytest_args.append(f"-m {args.marker}")
    
    # 运行pytest
    print(f"开始运行测试，环境: {args.env}")
    print(f"测试报告将保存到: {report_dir}")
    
    exit_code = pytest.main(pytest_args)
    
    # 生成allure报告（需要系统安装allure命令行工具）
    if os.path.exists(args.allure) and len(os.listdir(args.allure)) > 0:
        allure_report_dir = os.path.join(report_dir, "allure-report")
        os.system(f"allure generate {args.allure} -o {allure_report_dir} --clean")
        print(f"Allure报告已生成: {allure_report_dir}")
    
    return exit_code

if __name__ == "__main__":
    run_tests()
