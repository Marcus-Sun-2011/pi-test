import unittest
import sys
import os

# Ensure the current project root is in sys.path so 'src' can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.core.workspace import workspace_manager
from src.tools.registry import registry
from src.tools.implementations.file_tool import FileReadTool

class TestCoreComponents(unittest.TestCase):
    def test_workspace_manager_success(self):
        # 测试基础路径逻辑（确保它能识别当前目录内的文件）
        test_path = "some_local_file.txt"
        self.assertTrue(workspace_manager.is_safe_path(test_path))

    def test_workspace_manager_security(self):
        # 验证安全性：严禁跨越出当前目录的路径
        unsafe_paths = ["../secret.txt", "../../etc/passwd", "/usr/bin/python"]
        for path in unsafe_paths:
            with self.subTest(path=path):
                try:
                    workspace_manager.get_safe_path(path)
                    self.fail(f"Security failure: {path} was not caught as unsafe.")
                except PermissionError:
                    pass # 成功捕获到了安全风险

    def test_tool_registry(self):
        # 验证可以从注册表中获取到已注册的工具
        fetched_tool = registry.get_tool("read_file")
        self.assertEqual(fetched_tool.name, "read_file")

        web_tool = registry.get_tool("web_search")
        self.assertEqual(web_tool.name, "web_search")

        time_tool = registry.get_tool("get_current_time")
        self.assertEqual(time_tool.name, "get_current_time")
        
        # Test executing time tool
        res = time_tool.execute()
        self.assertEqual(res["status"], "success")
        self.assertTrue(len(res["result"]) > 0)
        
        # 验证不存在的工具应当抛出 ValueError
        with self.assertRaises(ValueError):
            registry.get_tool("non_existent_tool")

if __name__ == "__main__":
    unittest.main()
