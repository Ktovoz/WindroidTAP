import pyautogui
from loguru import logger
from typing import Optional
from PIL.Image import Image
from base import BaseWindowOperations

class MouseOperations(BaseWindowOperations):
    _ALLOWED_BUTTONS = {'left', 'right'}

    @BaseWindowOperations.check_activation
    def screenshot(self, save_path: Optional[str] = None) -> Optional[Image]:
        try:
            left, top, width, height = self._get_window_rect()
            img = pyautogui.screenshot(region=(left, top, width, height))
            if save_path:
                img.save(save_path)
                logger.debug("截图保存成功: {}", save_path)
            return img
        except pyautogui.ImageNotFoundException:
            logger.error("截图区域不可见")
            return None

    @BaseWindowOperations.check_activation
    def click(self, x: int, y: int,
              button: str = 'left', duration: float = 0) -> None:
        if button not in self._ALLOWED_BUTTONS:
            raise ValueError(f"无效按钮类型: {button}")

        abs_x, abs_y = self._calc_abs_pos(x, y)
        pyautogui.click(abs_x, abs_y, button=button, duration=duration)
        logger.debug("点击坐标 ({}, {}) {}", abs_x, abs_y, button)

    @BaseWindowOperations.check_activation
    def drag(self, start_x: int, start_y: int,
             end_x: int, end_y: int, button: str = 'left') -> None:
        if button not in self._ALLOWED_BUTTONS:
            raise ValueError(f"无效按钮类型: {button}")

        left, top, _, _ = self._get_window_rect()
        abs_s = (left + start_x, top + start_y)
        abs_e = (left + end_x, top + end_y)

        pyautogui.moveTo(*abs_s)
        pyautogui.mouseDown(button=button)
        pyautogui.moveTo(*abs_e, duration=0.25)
        pyautogui.mouseUp(button=button)
        logger.debug("拖拽完成 {}→{}", abs_s, abs_e)