from typing import Optional, Union, List, Tuple
from .app import App
from .win import WindowUtils
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
        self._app = App(ip=ip, port=port)
        self.click = self._app.click
        self.input_text = self._app.input_text
        self.screenshot = self._app.capture_jpg
        self.swipe = self._app.swipe
        self.get_size = self._app.get_size
        
        # APP平台不支持的方法
        def _not_supported(*args, **kwargs):
            raise NotImplementedError("APP平台不支持此操作")
        self.press_keys = _not_supported
        self.hotkey = _not_supported

    def _init_windows(self, window_title: Optional[str], window_handle: Optional[int]):
        """初始化Windows平台操作方法"""
        if window_handle:
            self._win = WindowUtils.create_operation(window_handle)
        else:
            self._win = WindowUtils.operate_window(window_title)
            if not self._win:
                raise ValueError(f"未找到标题包含 '{window_title}' 的窗口")
        
        # 映射方法
        self.click = lambda x, y: self._win.click(x, y)
        self.screenshot = self._win.screenshot
        self.swipe = self._win.drag
        self.input_text = self._win.type_text
        self.press_keys = self._win.press_key
        self.hotkey = self._win.hotkey
        
        def _get_win_size():
            rect = self._win._get_window_rect()
            return (rect[2], rect[3]) if rect else None
        self.get_size = _get_win_size 