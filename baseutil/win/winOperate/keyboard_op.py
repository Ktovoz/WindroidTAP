import time
import keyboard
from loguru import logger
from typing import Union, List
from base import BaseWindowOperations

class KeyboardOperations(BaseWindowOperations):
    @BaseWindowOperations.check_activation
    def type_text(self, text: str, interval: float = 0.02) -> None:
        keyboard.write(text, delay=interval)
        logger.debug("文本输入: {}", text[:20] + '...' if len(text) > 20 else text)

    @BaseWindowOperations.check_activation
    def press_key(self, keys: Union[str, List[str]],
                  presses: int = 1, interval: float = 0.1) -> None:
        if isinstance(keys, str):
            keys = [keys]
        for _ in range(presses):
            for key in keys:
                keyboard.press(key)
                keyboard.release(key)
                time.sleep(interval)
        logger.debug("按键操作: {}x{}", keys, presses)

    @BaseWindowOperations.check_activation
    def hotkey(self, *keys: str) -> None:
        for key in keys:
            keyboard.press(key)
        for key in reversed(keys):
            keyboard.release(key)
        logger.debug("组合键执行: {}", keys)