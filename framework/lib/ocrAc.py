from typing import List, Set, Tuple, Optional, Union
from loguru import logger
from .imgTool import ImageProcessor
from .paddlTool import PaddleOCRTool


class OcrActions:
    """
    OCR操作类，提供图像文本识别相关功能。
    
    主要功能：
    - 设置和管理感兴趣区域(ROI)
    - 文本搜索和验证
    - 批量文本提取和匹配
    """

    def __init__(self, region_of_interest: Optional[List[List[int]]] = None):
        """
        初始化OCR操作对象
        
        Args:
            region_of_interest: 感兴趣区域的坐标点列表，格式为[[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
        """
        self.region_of_interest = region_of_interest
        self.image_processor = ImageProcessor()
        self.paddle_ocr = PaddleOCRTool()  # 初始化 PaddleOCR 工具类实例

    def set_region_of_interest(self, point):
        """
        设置新的感兴趣区域。

        参数:
        point: 新的感兴趣区域的坐标点。
        """
        self.region_of_interest = point

    def _crop_image(self, image_input: Union[str, bytes]) -> Union[str, bytes]:
        """
        根据ROI裁剪图像
        
        Args:
            image_input: 输入图像路径或图像字节数据
            
        Returns:
            裁剪后的图像数据
        """
        try:
            if self.region_of_interest:
                return self.image_processor.crop_image_by_corners(image_input, self.region_of_interest)
            return image_input
        except Exception as e:
            logger.error(f"图像裁剪失败: {e}")
            return image_input

    def _validate_input(self, image_input: Union[str, bytes], text: Union[str, List[str]]) -> bool:
        """
        验证输入参数的有效性
        
        Args:
            image_input: 输入图像
            text: 待搜索的文本或文本列表
            
        Returns:
            bool: 输入是否有效
        """
        if not isinstance(image_input, (str, bytes)):
            logger.error(f"无效的图像输入类型: {type(image_input)}")
            return False
            
        if isinstance(text, str):
            return True
        elif isinstance(text, list):
            return all(isinstance(t, str) for t in text)
        return False

    def ocr_search_text(self, image_input: Union[str, bytes], search_text: str) -> Optional[Tuple]:
        """
        在图像中搜索指定文本
        
        Args:
            image_input: 输入图像
            search_text: 要搜索的文本
            
        Returns:
            Optional[Tuple]: 匹配到的文本信息，未找到则返回None
        """
        if not self._validate_input(image_input, search_text):
            return None
            
        try:
            cropped_image = self._crop_image(image_input)
            return self.paddle_ocr.filter_and_select_text(cropped_image, search_text)
        except Exception as e:
            logger.error(f"OCR搜索文本失败: {e}, 图像: {image_input}, 搜索文本: {search_text}")
            return None

    def ocr_extract_all_text(self, image_input: Union[str, bytes]) -> List[Tuple]:
        """
        提取图像中的所有文本
        
        Args:
            image_input: 输入图像
            
        Returns:
            List[Tuple]: 识别到的所有文本信息列表
        """
        if not isinstance(image_input, (str, bytes)):
            logger.error(f"无效的图像输入类型: {type(image_input)}")
            return []
            
        try:
            cropped_image = self._crop_image(image_input)
            return self.paddle_ocr.filter_ocr_results(cropped_image)
        except Exception as e:
            logger.error(f"提取所有文本失败: {e}, 图像: {image_input}")
            return []

    def contains_all_texts(self, image_input: Union[str, bytes], texts_to_find: List[str]) -> bool:
        """
        检查图像是否包含所有指定文本
        
        Args:
            image_input: 输入图像
            texts_to_find: 要查找的文本列表
            
        Returns:
            bool: 是否包含所有指定文本
        """
        if not self._validate_input(image_input, texts_to_find):
            return False
            
        try:
            ocr_results = self.ocr_extract_all_text(image_input)
            found_texts: Set[str] = set()
            
            for item in ocr_results:
                recognized_text = item[1][0]
                logger.debug(f"识别到文本: {recognized_text}")
                for search_text in texts_to_find:
                    if search_text in recognized_text:
                        found_texts.add(search_text)
                        
            return found_texts == set(texts_to_find)
        except Exception as e:
            logger.error(f"文本匹配失败: {e}, 图像: {image_input}, 待查找文本: {texts_to_find}")
            return False

    def ocr_is_text_present(self, image_input: Union[str, bytes], search_text: str) -> bool:
        """
        检查指定文本是否存在于图像中
        
        Args:
            image_input: 输入图像
            search_text: 要查找的文本
            
        Returns:
            bool: 文本是否存在
        """
        return bool(self.ocr_search_text(image_input, search_text))


if __name__ == '__main__':
    corners = [[545, 920], [752, 920], [752, 951], [545, 951]]
    IMG_DIR = r"D:\temp"
    char = {'空白'}
    m1 = OcrActions()
    src = fr"{IMG_DIR}\screenshot_5cc8dda0-289f-468d-9885-474e480090c1.png"
    # cahr = m1.ocr_is_text(src, '神秘')
    # all = m1.ocr_all_text(src)
    # print(all)
    # print(m1.contains_texts(src, char))
    print(m1.contains_all_texts(src, char))
