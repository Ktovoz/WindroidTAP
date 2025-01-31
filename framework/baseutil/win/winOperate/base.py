import time
from functools import wraps
import win32gui
import pywintypes
from loguru import logger
from typing import Optional, Tuple

class BaseWindowOperations:
    _RECT_CACHE_TIME = 0.2  # 窗口坐标缓存时间(秒)

    def __init__(self, hwnd: int, auto_activate: bool = True):
        self.hwnd = hwnd
        self.auto_activate = auto_activate
        self._rect_cache = (0, 0, 0, 0)
        self._last_rect_time = 0

    def _get_window_rect(self, force: bool = False) -> Tuple[int, int, int, int]:
        if force or (time.time() - self._last_rect_time > self._RECT_CACHE_TIME):
            try:
                left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
                self._rect_cache = (left, top, right - left, bottom - top)
                self._last_rect_time = time.time()
            except pywintypes.error as e:
                logger.error("获取窗口坐标失败: {}", e)
                raise RuntimeError("窗口句柄已失效") from e
        return self._rect_cache

    def _calc_abs_pos(self, x: int, y: int) -> Tuple[int, int]:
        left, top, _, _ = self._get_window_rect()
        return left + x, top + y

    def activate(self) -> bool:
        try:
            if win32gui.GetForegroundWindow() != self.hwnd:
                win32gui.SetForegroundWindow(self.hwnd)
                self._get_window_rect(force=True)  # 激活后强制更新坐标
                logger.debug("窗口激活成功 hwnd: {}", self.hwnd)
            return True
        except (pywintypes.error, RuntimeError) as e:
            logger.error("窗口激活失败: {}", e)
            return False

    def _should_activate(self, local_setting: Optional[bool]) -> bool:
        return self.auto_activate if local_setting is None else local_setting

    def _try_activate(self, auto_activate: Optional[bool]) -> bool:
        return self.activate() if self._should_activate(auto_activate) else True

    @classmethod
    def check_activation(cls, func):
        @wraps(func)
        def wrapper(self, *args, auto_activate=None, **kwargs):
            if not self._try_activate(auto_activate):
                return None
            try:
                return func(self, *args, **kwargs)
            except RuntimeError as e:
                logger.error("操作执行失败: {}", e)
            return None
        return wrapper