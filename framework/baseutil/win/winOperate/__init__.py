from .base import BaseWindowOperations
from .keyboard_op import KeyboardOperations
from .mouse_op import MouseOperations

class WindowOperations(BaseWindowOperations):
    def __init__(self, hwnd: int, auto_activate: bool = True):
        super().__init__(hwnd=hwnd, auto_activate=auto_activate)
        self._keyboard: KeyboardOperations = KeyboardOperations(hwnd, auto_activate)
        self._mouse: MouseOperations = MouseOperations(hwnd, auto_activate)

    @property
    def keyboard(self) -> KeyboardOperations:
        """获取键盘操作实例"""
        return self._keyboard
        
    @property 
    def mouse(self) -> MouseOperations:
        """获取鼠标操作实例"""
        return self._mouse

    # 键盘操作方法
    def type_text(self, text: str, interval: float = 0.02) -> None:
        return self._keyboard.type_text(text, interval=interval)

    def press_key(self, keys, presses: int = 1, interval: float = 0.1) -> None:
        return self._keyboard.press_key(keys, presses=presses, interval=interval)

    def hotkey(self, *keys: str) -> None:
        return self._keyboard.hotkey(*keys)

    # 鼠标操作方法
    def screenshot(self, save_path=None):
        return self._mouse.screenshot(save_path)

    def click(self, x: int, y: int, button: str = 'left', duration: float = 0) -> None:
        return self._mouse.click(x, y, button=button, duration=duration)

    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int, button: str = 'left') -> None:
        return self._mouse.drag(start_x, start_y, end_x, end_y, button=button)

__all__ = ['WindowOperations']
