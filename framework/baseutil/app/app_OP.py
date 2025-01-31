import requests
from typing import Tuple, Union
import time
from loguru import logger

class AppOperator:
    """APP操作类，用于控制设备的各种操作"""
    
    def __init__(self, ip: str, port: int = 8080):
        """
        初始化操作类
        
        Args:
            ip: 设备IP地址
            port: 端口号，默认8080
        """
        self.base_url = f"http://{ip}:{port}"
        logger.debug(f"初始化AppOperator，连接地址：{self.base_url}")
        self._check_connection()
    
    def _check_connection(self) -> bool:
        """检查连接是否正常"""
        try:
            response = self.test()
            return response.get('code') == "200"
        except:
            raise ConnectionError("无法连接到设备服务器")

    def _get(self, endpoint: str, params: dict = None) -> Union[dict, bytes]:
        """发送GET请求"""
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, params=params)
        if endpoint in ['cappng', 'capjpg', 'caplow']:
            return response.content
        return response.json()

    def test(self) -> dict:
        """测试连接"""
        return self._get('test')

    def find_device(self, mac: str) -> dict:
        """查找设备"""
        return self._get('findDevice', {'mac': mac})

    def connect(self) -> dict:
        """连接设备"""
        return self._get('connect')

    def get_size(self) -> Tuple[int, int]:
        """获取设备屏幕尺寸"""
        response = self._get('getSize')
        return response['width'], response['height']

    def click(self, x: int, y: int) -> dict:
        """点击指定坐标"""
        return self._get('click', {'x': x, 'y': y})

    def press(self) -> dict:
        """按下（按住不放）"""
        return self._get('press')

    def release(self) -> dict:
        """释放按压"""
        return self._get('release')

    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 1.0) -> dict:
        """
        滑动操作
        
        Args:
            start_x: 起始X坐标
            start_y: 起始Y坐标
            end_x: 结束X坐标
            end_y: 结束Y坐标
            duration: 持续时间(秒)
        """
        params = {
            'sec': duration,
            'x': start_x,
            'y': start_y,
            'ex': end_x,
            'ey': end_y
        }
        return self._get('swipe', params)

    def copy(self) -> dict:
        """复制操作"""
        return self._get('copy')

    def paste(self) -> dict:
        """粘贴操作"""
        return self._get('paste')

    def back(self) -> dict:
        """返回操作"""
        return self._get('back')

    def delete(self) -> dict:
        """删除操作"""
        return self._get('delete')

    def input_text(self, text: str) -> dict:
        """
        输入文本
        
        Args:
            text: 要输入的文本
        """
        return self._get('input', {'str': text})

    def home(self) -> dict:
        """点击Home键"""
        return self._get('home')

    def enter(self) -> dict:
        """点击回车键"""
        return self._get('enter')

    def capture_png(self) -> bytes:
        """截图并返回PNG格式"""
        return self._get('cappng')

    def capture_jpg(self) -> bytes:
        """截图并返回JPG格式"""
        return self._get('capjpg')

    def capture_low_quality(self) -> bytes:
        """截图并返回低质量JPG格式"""
        return self._get('caplow')
