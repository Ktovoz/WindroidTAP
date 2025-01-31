from framework.baseutil.platform_operator import PlatformOperator
from framework.lib.ocrAc import OcrActions
import time
from loguru import logger


def test_app_platform():
    logger.debug("=== 测试APP平台 ===")
    try:
        # 初始化APP平台操作器
        app = PlatformOperator('app', ip='192.168.31.228')

        # 测试基本操作
        logger.debug("测试点击操作...")
        app.click(100, 100)

        logger.debug("测试输入文本...")
        app.input_text("测试文本")

        logger.debug("测试滑动操作...")
        app.swipe(100, 200, 300, 400)

        logger.debug("测试获取屏幕尺寸...")
        size = app.get_size()
        logger.debug(f"屏幕尺寸: {size}")

        logger.debug("测试截图...")
        screenshot = app.screenshot()
        logger.debug(f"截图大小: {len(screenshot)} bytes")

        logger.debug("测试不支持的操作...")
        try:
            app.hotkey('ctrl', 'c')
        except NotImplementedError as e:
            logger.debug(f"预期的错误: {e}")

    except Exception as e:
        logger.debug(f"APP平台测试出错: {e}")


def test_windows_platform():
    logger.debug("=== 测试Windows平台 ===")
    try:
        # 初始化Windows平台操作器
        win = PlatformOperator('windows', window_title="记事本")

        # 测试基本操作
        logger.debug("测试点击操作...")
        win.click(100, 100)

        logger.debug("测试输入文本...")
        win.input_text("测试文本")
        time.sleep(1)  # 等待输入完成

        logger.debug("测试组合键...")
        win.hotkey('ctrl', 'a')  # 全选
        time.sleep(0.5)
        win.hotkey('ctrl', 'c')  # 复制
        time.sleep(0.5)

        logger.debug("测试滑动操作...")
        win.swipe(100, 200, 300, 400)

        logger.debug("测试获取窗口尺寸...")
        size = win.get_size()
        logger.debug(f"窗口尺寸: {size}")

        logger.debug("测试截图...")
        screenshot = win.screenshot()
        logger.debug(f"截图类型: {type(screenshot)}")

    except Exception as e:
        logger.debug(f"Windows平台测试出错: {e}")


def test_invalid_platform():
    logger.debug("=== 测试无效平台 ===")
    try:
        PlatformOperator('invalid')
    except ValueError as e:
        logger.debug(f"预期的错误: {e}")


def test_missing_params():
    logger.debug("=== 测试缺少参数 ===")
    try:
        PlatformOperator('app')  # 没有提供ip
    except ValueError as e:
        logger.debug(f"预期的错误 (APP无IP): {e}")

    try:
        PlatformOperator('windows')  # 没有提供window_title或handle
    except ValueError as e:
        logger.debug(f"预期的错误 (Windows无标题): {e}")


if __name__ == "__main__":
    logger.debug("开始测试 PlatformOperator...")

    # 测试无效平台和缺少参数
    test_invalid_platform()
    test_missing_params()

    # 测试APP平台
    # 注意：需要确保APP服务器在运行，否则会连接失败
    test_app_platform()

    # 测试Windows平台
    # 注意：需要打开一个记事本窗口进行测试
    test_windows_platform()

    logger.debug("测试完成!")
