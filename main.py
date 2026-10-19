"""测试入口。

用法：
    python main.py           # 运行全部用例并生成 allure 报告
    python main.py <path>    # 运行指定目录/文件
"""

import os
import sys

import pytest


def main():
    # 从命令行透传额外参数（如指定测试目录）
    args = list(sys.argv[1:])
    base_args = ["-s", "--clean-alluredir", "--alluredir=allure-results"]
    exit_code = pytest.main(base_args + args)

    # 生成 allure 报告（allure CLI 需已安装并加入 PATH）
    if os.system("allure --version") == 0:
        os.system("allure generate -c -o allure-report allure-results")
    else:
        print("警告：未检测到 allure CLI，跳过报告生成。请运行 `allure serve allure-results` 查看。")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
