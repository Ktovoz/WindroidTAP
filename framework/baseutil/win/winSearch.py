from loguru import logger
import win32gui
from typing import Optional, List, Tuple


class winSearch:
    def find_windows(self, name: Optional[str] = None) -> List[Tuple[str, int]]:
        result = []
        pattern = name.lower() if name else None

        def callback(hwnd, _):
            if (win32gui.IsWindowVisible(hwnd) and
                    win32gui.IsWindowEnabled(hwnd) and
                    (title := win32gui.GetWindowText(hwnd)) and
                    (not pattern or pattern in title.lower())):
                result.append((title, hwnd))

        win32gui.EnumWindows(callback, None)
        logger.debug(f"找到 {len(result)} 个{'匹配' if name else '可见'}窗口")
        return result


if __name__ == "__main__":
    result = winSearch().find_windows("py")
    for title, hwnd in result:
        logger.debug(f"{title} | {hwnd}")
