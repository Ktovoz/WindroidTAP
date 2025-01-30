from typing import Optional, Union, List, Tuple
from PIL.Image import Image
from .app.app_OP import AppOperator
from .win.winOperate.mouse_op import MouseOperations
from .win.winOperate.keyboard_op import KeyboardOperations
from loguru import logger

class PlatformOperator:
    """平台操作封装类，根据平台类型选择对应的操作方法"""
    
    def __init__(self, platform: str, **kwargs):
        """
        初始化平台操作类
        
        Args:
            platform: 平台类型 ('app' 或 'windows')
            **kwargs: 
                对于APP平台: ip, port(可选)
                对于Windows平台: window_title 或 window_handle
        """
        self.platform = platform.lower()
        logger.debug(f"初始化PlatformOperator，平台类型：{self.platform}")
        
        if self.platform not in ['app', 'windows']:
            raise ValueError("不支持的平台类型，只支持 'app' 或 'windows'")
            
        if self.platform == 'app':
            ip = kwargs.get('ip')
            if not ip:
                raise ValueError("APP平台需要提供ip参数")
            port = kwargs.get('port', 8080)
            logger.debug(f"初始化APP平台操作，IP：{ip}，端口：{port}")
            self._init_app(ip, port)
        else:
            window_title = kwargs.get('window_title')
            window_handle = kwargs.get('window_handle')
            if not (window_title or window_handle):
                raise ValueError("Windows平台需要提供window_title或window_handle参数")
            logger.debug(f"初始化Windows平台操作，窗口标题：{window_title}，窗口句柄：{window_handle}")
            self._init_windows(window_title, window_handle)

    def _init_app(self, ip: str, port: int):
        """初始化APP平台操作方法"""
        operator = AppOperator(ip=ip, port=port)
        self.click = operator.click
        self.input_text = operator.input_text
        self.screenshot = operator.capture_png
        self.swipe = operator.swipe
        self.get_size = operator.get_size
        
        # APP平台不支持的方法
        def _not_supported(*args, **kwargs):
            raise NotImplementedError("APP平台不支持此操作")
        self.press_keys = _not_supported
        self.hotkey = _not_supported

    def _init_windows(self, window_title: Optional[str], window_handle: Optional[int]):
        """初始化Windows平台操作方法"""
        mouse_op = MouseOperations(window_title=window_title, window_handle=window_handle)
        keyboard_op = KeyboardOperations(window_title=window_title, window_handle=window_handle)
        
        self.click = mouse_op.click
        self.screenshot = mouse_op.screenshot
        self.swipe = mouse_op.drag
        self.input_text = keyboard_op.type_text
        self.press_keys = keyboard_op.press_key
        self.hotkey = keyboard_op.hotkey
        
        def _get_win_size():
            rect = mouse_op._get_window_rect()
            return (rect[2], rect[3]) if rect else None
        self.get_size = _get_win_size 