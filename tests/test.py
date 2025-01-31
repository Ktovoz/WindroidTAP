import unittest
from unittest.mock import Mock, patch
import os
import sys
import time

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from framework.baseutil.platform_operator import PlatformOperator
from framework.lib.ocrAc import OcrActions

class TestOCRAndPlatformOperations(unittest.TestCase):
    """OCR和平台操作的白盒测试"""

    def setUp(self):
        """测试前的初始化设置"""
        # 初始化测试用的图像路径
        self.test_image_path = os.path.join(os.path.dirname(__file__), "test_resources", "test_image.png")
        
        # 创建OCR操作实例
        self.ocr = OcrActions()
        
        # 创建Windows平台操作实例 - 更新为记事本
        self.win_op = PlatformOperator(
            platform='windows',
            window_title='记事本'
        )
        
        # 启动记事本进程
        os.system('notepad.exe')
        time.sleep(1)  # 等待记事本启动

    def test_ocr_region_of_interest(self):
        """测试OCR感兴趣区域设置功能"""
        test_roi = [[100, 100], [200, 100], [200, 200], [100, 200]]
        self.ocr.set_region_of_interest(test_roi)
        self.assertEqual(self.ocr.region_of_interest, test_roi)

    @patch('baseutil.ocrAc.paddlTool.filter_and_select_text')
    def test_ocr_search_text(self, mock_filter):
        """测试OCR文本搜索功能"""
        # 模拟OCR识别结果
        mock_result = (
            [[100, 100], [150, 100], [150, 130], [100, 130]],
            ['测试文本'],
            0.95
        )
        mock_filter.return_value = mock_result

        # 执行测试
        result = self.ocr.ocr_search_text(self.test_image_path, "测试文本")
        self.assertEqual(result, mock_result)
        mock_filter.assert_called_once()

    @patch('baseutil.ocrAc.paddlTool.filter_ocr_results')
    def test_ocr_extract_all_text(self, mock_filter):
        """测试OCR文本提取功能"""
        # 模拟OCR识别结果
        mock_results = [
            (
                [[100, 100], [150, 100], [150, 130], [100, 130]],
                ['文本1'],
                0.95
            ),
            (
                [[200, 200], [250, 200], [250, 230], [200, 230]],
                ['文本2'],
                0.90
            )
        ]
        mock_filter.return_value = mock_results

        # 执行测试
        results = self.ocr.ocr_extract_all_text(self.test_image_path)
        self.assertEqual(results, mock_results)
        mock_filter.assert_called_once()

    def test_platform_operator_initialization(self):
        """测试平台操作器初始化"""
        # 测试Windows平台
        win_op = PlatformOperator(platform='windows', window_title='测试窗口')
        self.assertEqual(win_op.platform, 'windows')

        # 测试APP平台
        app_op = PlatformOperator(platform='app', ip='127.0.0.1', port=8080)
        self.assertEqual(app_op.platform, 'app')

        # 测试无效平台
        with self.assertRaises(ValueError):
            PlatformOperator(platform='invalid')

    @patch('baseutil.win.winOperate.mouse_op.MouseOperations')
    @patch('baseutil.win.winOperate.keyboard_op.KeyboardOperations')
    def test_windows_operations(self, mock_keyboard, mock_mouse):
        """测试Windows平台的操作功能"""
        # 设置模拟对象
        mock_mouse_instance = Mock()
        mock_keyboard_instance = Mock()
        mock_mouse.return_value = mock_mouse_instance
        mock_keyboard.return_value = mock_keyboard_instance

        # 测试点击操作
        self.win_op.click(100, 200)
        mock_mouse_instance.click.assert_called_with(100, 200)

        # 测试文本输入
        self.win_op.input_text("测试文本")
        mock_keyboard_instance.type_text.assert_called_with("测试文本")

        # 测试热键操作
        self.win_op.hotkey('ctrl', 'a')
        mock_keyboard_instance.hotkey.assert_called_with('ctrl', 'a')

    def test_ocr_text_validation(self):
        """测试OCR文本验证功能"""
        # 测试无效输入
        self.assertFalse(self.ocr._validate_input(123, "测试"))  # 无效的图像输入
        self.assertFalse(self.ocr._validate_input("test.png", 123))  # 无效的文本输入
        self.assertTrue(self.ocr._validate_input("test.png", "测试"))  # 有效输入
        self.assertTrue(self.ocr._validate_input("test.png", ["测试1", "测试2"]))  # 有效的文本列表

    @patch('baseutil.ocrAc.imgTool.crop_image_by_corners')
    def test_image_cropping(self, mock_crop):
        """测试图像裁剪功能"""
        # 设置ROI并测试裁剪
        test_roi = [[0, 0], [100, 0], [100, 100], [0, 100]]
        self.ocr.set_region_of_interest(test_roi)
        
        mock_crop.return_value = b"cropped_image_data"
        result = self.ocr._crop_image("test.png")
        
        mock_crop.assert_called_with("test.png", test_roi)
        self.assertEqual(result, b"cropped_image_data")

    def test_notepad_interactions(self):
        """测试与记事本的实际交互"""
        test_text = "这是一段测试文本\n包含多行内容\n用于测试记事本操作"
        
        # 测试文本输入
        self.win_op.input_text(test_text)
        time.sleep(0.5)
        
        # 测试全选操作
        self.win_op.hotkey('ctrl', 'a')
        time.sleep(0.5)
        
        # 测试复制操作
        self.win_op.hotkey('ctrl', 'c')
        time.sleep(0.5)
        
        # 测试删除操作
        self.win_op.input_text('{BACKSPACE}')
        time.sleep(0.5)
        
        # 测试粘贴操作
        self.win_op.hotkey('ctrl', 'v')
        time.sleep(0.5)

    def tearDown(self):
        """测试后的清理工作"""
        # 关闭记事本而不保存
        self.win_op.hotkey('alt', 'f4')
        time.sleep(0.5)
        self.win_op.input_text('n')  # 在弹出的保存对话框中选择"不保存"
        
        super().tearDown()

if __name__ == '__main__':
    unittest.main(verbosity=2)
