from framework.baseutil.platform_operator import PlatformOperator
from framework.lib.ocrAc import OcrActions
from loguru import logger
import time

def android_automation_example():
    """
    Android平台自动化示例
    演示如何结合OCR和平台操作实现APP自动化操作
    """
    # 初始化Android平台操作器
    app_op = PlatformOperator(
        platform='app',
        ip='127.0.0.1',  # 根据实际设备IP修改
        port=8080        # 根据实际端口修改
    )
    
    # 初始化OCR操作器
    ocr = OcrActions()
    
    try:
        # 获取屏幕尺寸
        screen_size = app_op.get_size()
        logger.info(f"屏幕尺寸: {screen_size}")
        
        # 截取当前屏幕
        screenshot = app_op.screenshot()
        
        # 查找并点击特定文本
        text_to_find = "开始"
        if ocr.ocr_is_text_present(screenshot, text_to_find):
            logger.info(f"找到文本: {text_to_find}")
            
            # 获取文本位置并点击
            text_location = ocr.ocr_search_text(screenshot, text_to_find)
            if text_location:
                # 计算点击坐标
                center_x = (text_location[0][0][0] + text_location[0][2][0]) // 2
                center_y = (text_location[0][0][1] + text_location[0][2][1]) // 2
                app_op.click(center_x, center_y)
                logger.info(f"点击坐标: ({center_x}, {center_y})")
        
        # 等待新界面加载
        time.sleep(2)
        
        # 在特定区域内搜索文本
        roi = [[100, 100], [300, 100], [300, 200], [100, 200]]  # 示例ROI区域
        ocr.set_region_of_interest(roi)
        
        # 再次截图并在ROI区域内搜索文本
        screenshot = app_op.screenshot()
        target_texts = ["设置", "个人信息"]
        if ocr.contains_all_texts(screenshot, target_texts):
            logger.info("在指定区域内找到所有目标文本")
            
        # 模拟滑动操作
        app_op.swipe(500, 1000, 500, 200)  # 上滑操作
        time.sleep(1)
        
        # 输入文本
        app_op.input_text("测试文本输入")
        
    except Exception as e:
        logger.error(f"自动化过程出错: {e}")

if __name__ == "__main__":
    android_automation_example() 