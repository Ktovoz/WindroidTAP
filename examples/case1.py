from framework.baseutil.platform_operator import PlatformOperator
from framework.lib.ocrAc import OcrActions
from loguru import logger
import time

def windows_automation_example():
    """
    Windows平台自动化示例
    演示如何结合OCR和平台操作实现自动化点击和文本验证
    """
    # 初始化Windows平台操作器（以记事本为例）
    win_op = PlatformOperator(
        platform='windows',
        window_title='记事本'
    )
    
    # 初始化OCR操作器
    ocr = OcrActions()
    
    try:
        # 1. 点击文本区域准备输入
        win_op.click(50, 50)
        win_op.input_text("=== 自动化测试开始 ===\n")
        time.sleep(0.5)
        
        # 2. 输入多行示例文本
        sample_text = """第一行：这是测试文本
第二行：特殊符号 !@#$%^&*()
第三行：数字测试 1234567890
"""
        win_op.input_text(sample_text)
        time.sleep(1)
        
        # 3. 截图并验证文本
        screenshot = win_op.screenshot()
        
        # 验证多个文本是否存在
        texts_to_find = ["第一行", "特殊符号", "数字测试"]
        if ocr.contains_all_texts(screenshot, texts_to_find):
            logger.info("成功找到所有指定文本")
            
            # 获取特定文本位置并点击（比如点击"数字测试"）
            text_location = ocr.ocr_search_text(screenshot, "数字测试")
            if text_location:
                center_x = (text_location[0][0][0] + text_location[0][2][0]) // 2
                center_y = (text_location[0][0][1] + text_location[0][2][1]) // 2
                win_op.click(center_x, center_y)
                logger.info(f"点击坐标: ({center_x}, {center_y})")
        
        # 4. 使用快捷键操作
        # 全选文本
        win_op.hotkey('ctrl', 'a')
        time.sleep(0.5)
        
        # 复制文本
        win_op.hotkey('ctrl', 'c')
        logger.debug("已复制全部内容")
        
        # 新建文件
        win_op.hotkey('ctrl', 'n')
        time.sleep(1)
        
        # 粘贴内容
        win_op.hotkey('ctrl', 'v')
        win_op.input_text("\n=== 粘贴内容结束 ===")
        
        # 保存截图
        screenshot = win_op.screenshot()
        
        # 5. 保存文件操作
        win_op.hotkey('ctrl', 's')
        time.sleep(1)  # 等待保存对话框
        win_op.input_text("automation_test.txt")
        time.sleep(0.5)
        win_op.press_keys('enter')
        
        logger.success("自动化操作完成")
        
    except Exception as e:
        logger.error(f"自动化过程出错: {e}")

if __name__ == "__main__":
    # 配置日志格式
    logger.add("notepad_auto.log",
               format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
               rotation="10 MB")
               
    windows_automation_example()
