import os
import re
from PIL import Image
from paddleocr import PaddleOCR, draw_ocr
from loguru import logger

class PaddleOCRTool:
    def __init__(self):
        """
        初始化 PaddleOCR 工具类
        """
        dir = os.path.dirname(__file__)
        self.ocr = PaddleOCR(
            lang='ch',
            rec_char_dict_path=f'{dir}/ppocr_keys_v1.txt',
            det_model_dir=f'{dir}/ch_PP-OCRv4_det_infer',
            rec_model_dir=f'{dir}/ch_PP-OCRv4_rec_infer',
            cls_model_dir=f'{dir}/ch_ppocr_mobile_v2.0_cls_infer',
            cls=False,
            use_angle_cls=False,
            use_tensorrt=True,
            enable_mkldnn=True,
            use_mp=True,
            total_process_num=6
        )
        logger.debug("OCR模型加载完成")

    def filter_ocr_results(self, img_path, confidence_threshold=0.8):
        """
        对给定的图像进行 OCR 识别，并筛选出置信度大于指定阈值的结果。

        :param img_path: 图像文件路径
        :param confidence_threshold: 置信度阈值，默认为 0.8
        :return: 筛选后的结果列表
        """
        try:
            logger.debug(f"开始OCR识别，图片路径: {img_path}, 置信度阈值: {confidence_threshold}")
            
            if not os.path.exists(img_path):
                logger.error(f"图片文件不存在: {img_path}")
                return []
                
            result = self.ocr.ocr(img_path)[0]
            logger.debug(f"OCR识别完成，原始结果数量: {len(result)}")
            
            filtered_result = [
                item for item in result if item[1][1] > confidence_threshold
            ]
            logger.debug(f"筛选后结果数量: {len(filtered_result)}")
            return filtered_result
            
        except Exception as e:
            logger.error(f"OCR识别发生错误: {str(e)}")
            return []

    def process_image(self, img1, result, font_path=None):
        """
        处理图像并保存结果。

        参数:
            img1 (str): 图像文件路径。
            result (list): 包含检测结果的列表，每个元素为 (box, (text, score))。
            font_path (str): 字体文件路径，默认为None时会使用系统默认字体。

        返回:
            bool: 处理成功返回True，失败返回False
        """
        try:
            logger.debug(f"开始处理图像: {img1}")
            
            if not os.path.exists(img1):
                logger.error(f"输入图片不存在: {img1}")
                return False
                
            # 打开并转换图像
            image = Image.open(img1).convert('RGB')
            
            if not result:
                logger.warning("OCR结果为空，无法处理图像")
                return False

            # 提取检测结果
            boxes = [line[0] for line in result]
            txts = [line[1][0] for line in result]
            scores = [line[1][1] for line in result]

            logger.debug(f"检测到文本数量: {len(txts)}")
            
            # 绘制 OCR 结果
            im_show = draw_ocr(image, boxes, txts, scores, font_path=font_path)
            im_show = Image.fromarray(im_show)

            # 保存结果图像
            output_path = 'result.jpg'
            im_show.save(output_path)
            logger.debug(f"结果图像已保存至: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"处理图像时发生错误: {str(e)}")
            return False

    def filter_and_select_text(self, img_path, pattern, pattern_type='char'):
        """
        根据给定的字符或正则表达式筛选列表中的文本，并返回筛选后的文本和其对应的框。

        :param img_path: 图像文件路径
        :param pattern: 需要匹配的字符或正则表达式
        :param pattern_type: 指定 `pattern` 是字符 ('char') 还是正则表达式 ('regex')，默认为 'char'
        :return: 匹配的文本及其对应的框，或 None
        """
        try:
            logger.debug(f"开始文本筛选，图片: {img_path}, 模式: {pattern}, 类型: {pattern_type}")
            
            pattern_type = pattern_type.lower()
            if pattern_type not in ['char', 'regex']:
                logger.error(f"无效的pattern_type: {pattern_type}")
                raise ValueError("pattern_type 必须是 'char' 或 'regex'")
                
            data = self.filter_ocr_results(img_path)
            if not data:
                logger.warning("OCR结果为空")
                return None

            # 根据给定的字符或正则表达式筛选列表中的文本
            if pattern_type == 'char':
                matched_items = [item for item in data if pattern in item[1][0]]
            else:  # regex
                try:
                    regex = re.compile(pattern)
                    matched_items = [item for item in data if regex.search(item[1][0])]
                except re.error as e:
                    logger.error(f"正则表达式编译错误: {str(e)}")
                    return None

            if not matched_items:
                logger.debug("没有找到匹配结果")
                return None

            # 按照置信度由高到低排序
            matched_items.sort(key=lambda x: x[1][1], reverse=True)
            selected_item = matched_items[0]
            logger.debug(f"找到最佳匹配: {selected_item[1][0]}, 置信度: {selected_item[1][1]}")
            return selected_item
            
        except Exception as e:
            logger.error(f"文本筛选过程中发生错误: {str(e)}")
            return None

if __name__ == '__main__':
    # 定义图片目录
    IMG_DIR = r"D:\temp"
    # 定义具体路径
    # back = fr"{IMG_DIR}\main\Landscape\1280x960.png"
    # back = fr"{IMG_DIR}\img/afkj/main/Landscape/1600x900.png"
    back = fr"D:\temp\imgbao\Snipaste_2024-12-03_14-00-34.png"
    # src = fr"{IMG_DIR}\guajijindu.png"
    src = fr"{IMG_DIR}\screenshot_5cc8dda0-289f-468d-9885-474e480090c1.png"
    # print(img3)
    result = filter_ocr_results(src)
    print(result)
    # process_image(img2, result)
    # char = r'阵容'
    # center = find_one_center_point_txt(back, char, 'char', True)
    # print(f"中心点坐标: {center}")
