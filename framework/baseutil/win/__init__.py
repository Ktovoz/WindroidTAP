from .winOperate import WindowOperations
from .winSearch import winSearch
from typing import Optional, List, Tuple, Union

class WindowUtils:
    """窗口工具类，集成窗口搜索和操作功能"""
    
    @staticmethod
    def find_windows(name: Optional[str] = None) -> List[Tuple[str, int]]:
        """
        查找窗口
        Args:
            name: 窗口标题（可选），支持模糊匹配
        Returns:
            返回匹配的窗口列表，每个元素为 (窗口标题, 窗口句柄) 的元组
        """
        return winSearch().find_windows(name)
    
    @classmethod
    def create_operation(cls, hwnd: int, auto_activate: bool = True) -> WindowOperations:
        """
        创建窗口操作实例
        Args:
            hwnd: 窗口句柄
            auto_activate: 是否自动激活窗口
        Returns:
            WindowOperations实例
        """
        return WindowOperations(hwnd, auto_activate)

    @classmethod
    def operate_window(cls, window_name: str) -> Optional[WindowOperations]:
        """
        通过窗口名称快速创建操作实例
        Args:
            window_name: 窗口标题，支持模糊匹配
        Returns:
            找到窗口时返回WindowOperations实例，否则返回None
        Raises:
            ValueError: 当找到多个匹配窗口时抛出异常
        """
        windows = cls.find_windows(window_name)
        if not windows:
            return None
        if len(windows) > 1:
            raise ValueError(f"找到多个匹配的窗口: {windows}")
        return cls.create_operation(windows[0][1])

    @classmethod
    def quick_click(cls, window_name: str, x: int, y: int, 
                   button: str = 'left', duration: float = 0) -> bool:
        """
        快速点击指定窗口的坐标
        Args:
            window_name: 窗口标题
            x: 横坐标
            y: 纵坐标
            button: 鼠标按键，'left'或'right'
            duration: 点击持续时间
        Returns:
            操作是否成功
        """
        if window := cls.operate_window(window_name):
            window.click(x, y, button, duration)
            return True
        return False

    @classmethod
    def quick_type(cls, window_name: str, text: str, 
                  interval: float = 0.02) -> bool:
        """
        快速在指定窗口输入文本
        Args:
            window_name: 窗口标题
            text: 要输入的文本
            interval: 输入间隔时间
        Returns:
            操作是否成功
        """
        if window := cls.operate_window(window_name):
            window.type_text(text, interval)
            return True
        return False

    @classmethod
    def quick_screenshot(cls, window_name: str, 
                        save_path: Optional[str] = None):
        """
        快速对指定窗口截图
        Args:
            window_name: 窗口标题
            save_path: 保存路径（可选）
        Returns:
            截图成功时返回Image对象，失败返回None
        """
        if window := cls.operate_window(window_name):
            return window.screenshot(save_path)
        return None

    @classmethod
    def quick_drag(cls, window_name: str, start_x: int, start_y: int,
                  end_x: int, end_y: int, button: str = 'left') -> bool:
        """
        快速在指定窗口进行拖拽操作
        Args:
            window_name: 窗口标题
            start_x: 起始横坐标
            start_y: 起始纵坐标
            end_x: 结束横坐标
            end_y: 结束纵坐标
            button: 鼠标按键，'left'或'right'
        Returns:
            操作是否成功
        """
        if window := cls.operate_window(window_name):
            window.drag(start_x, start_y, end_x, end_y, button)
            return True
        return False

    @classmethod
    def quick_press(cls, window_name: str, keys,
                   presses: int = 1, interval: float = 0.1) -> bool:
        """
        快速在指定窗口按键
        Args:
            window_name: 窗口标题
            keys: 按键或按键组合
            presses: 按键次数
            interval: 按键间隔时间
        Returns:
            操作是否成功
        """
        if window := cls.operate_window(window_name):
            window.press_key(keys, presses, interval)
            return True
        return False

    @classmethod
    def quick_hotkey(cls, window_name: str, *keys: str) -> bool:
        """
        快速在指定窗口执行热键组合
        Args:
            window_name: 窗口标题
            keys: 热键组合
        Returns:
            操作是否成功
        """
        if window := cls.operate_window(window_name):
            window.hotkey(*keys)
            return True
        return False

__all__ = ['WindowUtils']
