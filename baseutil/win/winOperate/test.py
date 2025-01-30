# notepad_demo.py
from rework.baseutil.win.winSearch import winSearch
from mouse_op import MouseOperations
from keyboard_op import KeyboardOperations
from loguru import logger
import time


def notepad_automation():
    """记事本自动化操作演示"""
    try:
        # 窗口搜索（确保已打开记事本）
        if not (results := winSearch().find_windows("记事本")):
            logger.error("请先打开记事本程序")
            return

        hwnd = results[0][1]
        logger.info(f"找到记事本窗口，句柄: {hwnd}")

        # 初始化控制器
        mouse = MouseOperations(hwnd, auto_activate=True)
        keyboard = KeyboardOperations(hwnd, auto_activate=True)

        # 操作序列 -------------------------------------------------
        # 1. 点击文本区域准备输入
        mouse.click(50, 50, duration=0.3)
        keyboard.type_text("=== 自动化测试开始 ===\n", interval=0.05)

        # 2. 输入多行文本
        sample_text = """第一行：基础文本输入
第二行：特殊符号 !@#$%^&*()
第三行：数字测试 1234567890
"""
        keyboard.type_text(sample_text)

        # 3. 使用快捷键全选+复制
        keyboard.hotkey('ctrl', 'a')
        keyboard.hotkey('ctrl', 'c')
        logger.debug("已复制全部内容")

        # 4. 新建文件（通过菜单操作）
        # 点击菜单栏 -> 文件 -> 新建
        mouse.click(15, 15)  # 点击菜单栏文件位置
        time.sleep(0.5)
        mouse.drag(15, 15, 15, 50)  # 模拟下拉菜单
        mouse.click(15, 80)  # 点击"新建"

        # 5. 粘贴内容并保存
        mouse.click(200, 200)  # 点击新文档区域
        keyboard.hotkey('ctrl', 'a')
        keyboard.press_key('delete', presses=2)
        keyboard.hotkey('ctrl', 'v')
        keyboard.type_text("\n=== 粘贴内容结束 ===")
        mouse.screenshot("windos.png")
        # 6. 保存文件（Ctrl+S）
        keyboard.hotkey('ctrl', 's')
        time.sleep(1)  # 等待保存对话框
        keyboard.type_text("automation_test.txt")
        keyboard.press_key('enter', presses=2, interval=0.5)

        logger.success("自动化操作完成")

    except Exception as e:
        logger.error(f"操作失败: {str(e)}")
    finally:
        logger.info("清理完成")


if __name__ == "__main__":
    # 配置日志格式
    logger.add("notepad_auto.log",
               format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
               rotation="10 MB")

    notepad_automation()