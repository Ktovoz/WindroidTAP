from .app_OP import AppOperator
from typing import Tuple, Union

class App:
    def __init__(self, ip: str, port: int = 8080):
        self._operator = AppOperator(ip, port)
    
    def find_device(self, mac: str) -> dict:
        """查找设备"""
        return self._operator.find_device(mac)
    
    def connect(self) -> dict:
        """连接设备"""
        return self._operator.connect()
    
    def get_size(self) -> Tuple[int, int]:
        """获取设备屏幕尺寸"""
        return self._operator.get_size()
    
    def click(self, x: int, y: int) -> dict:
        """点击指定坐标"""
        return self._operator.click(x, y)
    
    def press(self) -> dict:
        """按下（按住不放）"""
        return self._operator.press()
    
    def release(self) -> dict:
        """释放按压"""
        return self._operator.release()
    
    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 1.0) -> dict:
        """滑动操作"""
        return self._operator.swipe(start_x, start_y, end_x, end_y, duration)
    
    def copy(self) -> dict:
        """复制操作"""
        return self._operator.copy()
    
    def paste(self) -> dict:
        """粘贴操作"""
        return self._operator.paste()
    
    def back(self) -> dict:
        """返回操作"""
        return self._operator.back()
    
    def delete(self) -> dict:
        """删除操作"""
        return self._operator.delete()
    
    def input_text(self, text: str) -> dict:
        """输入文本"""
        return self._operator.input_text(text)
    
    def home(self) -> dict:
        """点击Home键"""
        return self._operator.home()
    
    def enter(self) -> dict:
        """点击回车键"""
        return self._operator.enter()
    
    def capture_png(self) -> bytes:
        """截图并返回PNG格式"""
        return self._operator.capture_png()
    
    def capture_jpg(self) -> bytes:
        """截图并返回JPG格式"""
        return self._operator.capture_jpg()
    
    def capture_low_quality(self) -> bytes:
        """截图并返回低质量JPG格式"""
        return self._operator.capture_low_quality()

__all__ = ['App']