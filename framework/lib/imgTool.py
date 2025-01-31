import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
from typing import Tuple, List, Optional, Union
from loguru import logger


class ImageProcessor:
    """图像处理工具类,提供图像操作相关功能"""
    
    @staticmethod
    def get_image_size(image: np.ndarray) -> Tuple[int, int]:
        """获取图片尺寸
        
        Args:
            image: OpenCV图像对象

        Returns:
            图片的宽度和高度元组 (width, height)
        
        Raises:
            ValueError: 当图片为空时抛出
        """
        try:
            if image is None:
                raise ValueError("输入图片不能为空")
            
            height, width = image.shape[:2]
            logger.debug(f"获取图片尺寸: width={width}, height={height}")
            return width, height
        except Exception as e:
            logger.debug(f"获取图片尺寸失败: {e}")
            raise

    @staticmethod 
    def image_to_array(image: np.ndarray) -> np.ndarray:
        """将图片转换为NumPy数组
        
        Args:
            image: OpenCV图像对象
            
        Returns:
            图片的数组表示
            
        Raises:
            ValueError: 当图片为空时抛出
        """
        try:
            if image is None:
                raise ValueError("输入图片不能为空")
            
            array = np.array(image)
            logger.debug(f"图片转换为数组: shape={array.shape}")
            return array
        except Exception as e:
            logger.debug(f"图片转换为数组失败: {e}")
            raise

    @staticmethod
    def check_image_orientation_and_size(img, return_orientation=False):
        """
        检查图片的方向和尺寸是否在固定的允许的尺寸列表内。

        参数:
        - image_path: 图片文件路径
        - return_orientation: 布尔值，决定是否返回图片的方向信息，默认为 False

        返回:
        - orientation: 如果 return_orientation 为 True，则返回 'horizontal' 或 'vertical'
        - is_allowed_size: True 或 False
        """
        # 固定的允许尺寸列表
        allowed_sizes = [(431, 777)]
        # allowed_sizes = [(1280, 720), (1280, 800)]

        if img is None:
            raise ValueError("无法读取图片，请检查路径是否正确")

        height, width = img.shape[:2]

        # 判断方向
        if width > height:
            orientation = 'horizontal'
        else:
            orientation = 'vertical'

        # 判断尺寸是否在允许的尺寸列表内
        is_allowed_size = (width, height) in allowed_sizes

        if return_orientation:
            return orientation, is_allowed_size
        else:
            return is_allowed_size

    @staticmethod
    def load_and_process_images(src_img: str, back_img: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """加载和预处理图像，检测特征点并计算单应性矩阵
        
        Args:
            src_img: 目标图像路径
            back_img: 背景图像路径
            
        Returns:
            包含处理后的图像、特征点和描述符的元组
            
        Raises:
            ValueError: 当图像无法读取或处理失败时抛出
            FileNotFoundError: 当图像文件不存在时抛出
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(src_img):
                raise FileNotFoundError(f"目标图像文件不存在: {src_img}")
            if not os.path.exists(back_img):
                raise FileNotFoundError(f"背景图像文件不存在: {back_img}")
            
            logger.debug(f"开始处理图像: src={src_img}, back={back_img}")
            
            # 读取图像并转换为灰度图
            img1 = cv2.imread(src_img, 0)
            img2 = cv2.imread(back_img, 0)
            if img1 is None or img2 is None:
                raise ValueError("无法读取图像，请检查图像路径是否正确。")
            
            logger.debug("成功读取图像")

            # 使用SIFT检测关键点和描述符
            sift = cv2.SIFT_create()
            kp1, des1 = sift.detectAndCompute(img1, None)
            kp2, des2 = sift.detectAndCompute(img2, None)
            if des1 is None or des2 is None:
                raise ValueError("未检测到足够的关键点，请检查输入图像。")
                
            logger.debug(f"检测到特征点: kp1={len(kp1)}, kp2={len(kp2)}")

            # 使用FLANN匹配器进行匹配
            index_params = dict(algorithm=1, trees=5)
            search_params = dict(checks=50)
            flann = cv2.FlannBasedMatcher(index_params, search_params)
            matches = flann.knnMatch(des1, des2, k=2)
            good_matches = [m for m, n in matches if m.distance < 0.7 * n.distance]
            if not good_matches:
                raise ValueError("未找到足够的匹配点，请检查输入图像。")
                
            logger.debug(f"找到有效匹配点: {len(good_matches)}")

            # 计算单应性矩阵
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            if M is None:
                raise ValueError("无法计算单应性矩阵，请检查输入图像。")
                
            logger.debug("成功计算单应性矩阵")

            # 计算目标图像的四个角点在背景图像中的位置
            h, w = img1.shape
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)
            
            logger.debug("完成图像处理")
            return img1, img2, dst
            
        except Exception as e:
            logger.debug(f"图像处理失败: {e}")
            raise

    @staticmethod
    def visualize_results(back_img: str, corners: List[Tuple[int, int]], show: bool = False, scale_factor: float = 0.8) -> None:
        """可视化匹配结果
        
        Args:
            back_img: 背景图像路径
            corners: 目标图像的四角坐标
            show: 是否显示匹配结果
            scale_factor: 缩放因子
        """
        if not show:
            return
            
        img3 = cv2.imread(back_img)
        new_width = int(img3.shape[1] * scale_factor)
        new_height = int(img3.shape[0] * scale_factor)
        img3 = cv2.resize(img3, (new_width, new_height))
        corners_scaled = [(int(x * scale_factor), int(y * scale_factor))
                          for x, y in corners]

        for corner in corners_scaled:
            cv2.circle(img3, corner, 6, (0, 0, 255), 2)

        cv2.line(img3, corners_scaled[0], corners_scaled[1], (0, 0, 255), 2)
        cv2.line(img3, corners_scaled[1], corners_scaled[2], (0, 0, 255), 2)
        cv2.line(img3, corners_scaled[2], corners_scaled[3], (0, 0, 255), 2)
        cv2.line(img3, corners_scaled[3], corners_scaled[0], (0, 0, 255), 2)

        cv2.imshow('Matched Image', img3)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def get_corners(src_img: str, back_img: str, show: bool = False) -> Optional[List[Tuple[int, int]]]:
        """在背景图像中查找目标图像的四角坐标
        
        Args:
            src_img: 目标图像路径
            back_img: 背景图像路径
            show: 是否显示匹配结果
            
        Returns:
            目标图像在背景中的四角坐标,如果失败返回None
        """
        try:
            logger.debug(f"开始获取角点: src={src_img}, back={back_img}")
            _, _, dst = ImageProcessor.load_and_process_images(src_img, back_img)
            corners = [(int(x), int(y)) for x, y in dst.reshape(-1, 2)]
            if show:
                ImageProcessor.visualize_results(back_img, corners, show)
            logger.debug(f"成功获取角点: {corners}")
            return corners
        except Exception as e:
            logger.debug(f"获取角点失败: {e}")
            return None

    @staticmethod
    def get_center_location(src_img, back_img, show=False):
        """
        使用SIFT算法在背景图像中查找目标图像，并返回目标图像的中心点坐标。

        :param src_img: 目标图像路径
        :param back_img: 背景图像路径
        :param show: 是否显示匹配结果，1 表示显示
        :return: 目标图像在背景图像中的中心点坐标 (x, y)
        """
        try:
            _, _, dst = ImageProcessor.load_and_process_images(src_img, back_img)
            x, y, w, h = cv2.boundingRect(dst)
            center_x = x + w / 2
            center_y = y + h / 2
            point = [int(center_x), int(center_y)]
            ImageProcessor.visualize_results(back_img, [(x, y), (x + w, y), (x + w, y + h),
                                     (x, y + h)], show)
            return point
        except Exception as e:
            print(f"发生错误: {e}")
            return None

    @staticmethod
    def capture_target_image_v1(src_img, back_img, show=False):
        '''
        使用SIFT和基于FLANN的匹配从背景图像中捕获目标图像。

        :param src_img: 目标图像的路径。
        :param back_img: 背景图像的路径。
        :param show: 如果为True，则显示目标图像和匹配区域。
        :return: 背景图像中目标图像的匹配区域。
        '''
        try:
            img2_colour = cv2.imread(back_img)
            _, _, dst = ImageProcessor.load_and_process_images(src_img, back_img)
            rect = cv2.minAreaRect(dst)
            box = cv2.boxPoints(rect)
            box = np.int32(box)
            padding = 10
            min_x, min_y = np.min(box, axis=0) - padding
            max_x, max_y = np.max(box, axis=0) + padding
            min_x = max(0, min_x)
            min_y = max(0, min_y)
            max_x = min(img2_colour.shape[1], max_x)
            max_y = min(img2_colour.shape[0], max_y)
            img3 = img2_colour[min_y:max_y, min_x:max_x]

            if show:
                cv2.imshow("Target Image", cv2.imread(src_img))
                cv2.imshow("Matched Region", img3)
                print(f"Target Image Size: {cv2.imread(src_img).shape}")
                print(f"Matched Region Size: {img3.shape}")
                cv2.waitKey(0)

            return img3
        except FileNotFoundError as e:
            print(f"文件错误: {e}")
        except ValueError as e:
            print(f"值错误: {e}")
        except cv2.error as e:
            print(f"OpenCV错误: {e}")
        except Exception as e:
            print(f"未知错误: {e}")

    @staticmethod
    def mark_target(src_img, back_img):
        try:
            # 读取图像
            img1 = cv2.imread(src_img)
            img2 = cv2.imread(back_img)

            if img1 is None:
                raise FileNotFoundError(f"目标图像文件 '{src_img}' 不存在或无法读取。")
            if img2 is None:
                raise FileNotFoundError(f"背景图像文件 '{back_img}' 不存在或无法读取。")

            # 转换为灰度图像
            img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

            # 使用模板匹配
            result = cv2.matchTemplate(img2_gray, img1_gray, cv2.TM_CCOEFF_NORMED)

            # 设置阈值
            threshold = 0.8

            # 找到匹配位置
            loc = np.where(result >= threshold)

            # 在背景图像上绘制矩形框
            for pt in zip(*loc[::-1]):
                cv2.rectangle(
                    img2, pt,
                    (pt[0] + img1_gray.shape[1], pt[1] + img1_gray.shape[0]),
                    (0, 0, 255), 2)

            # 显示结果
            plt.figure(figsize=(10, 10))
            plt.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
            plt.title('Detected Matches')
            plt.axis('off')
            plt.show()

        except FileNotFoundError as e:
            print(f"文件错误: {e}")
        except cv2.error as e:
            print(f"OpenCV错误: {e}")
        except ValueError as e:
            print(f"值错误: {e}")
        except Exception as e:
            print(f"未知错误: {e}")

    @staticmethod
    def save_target_capture(src_img, back_img, name='target'):
        """
        保存从背景图像中捕获的目标图像，并返回图像的相对路径。

        参数:
            src_img (str): 目标图像的路径。
            back_img (str): 背景图像的路径。
            name (str): 保存的文件名。默认值为 'target'。

        返回:
            str: 图像保存成功的相对路径；如果保存失败，返回空字符串。
        """
        try:
            # 捕获目标图像
            target_image = ImageProcessor.capture_target_image_v1(src_img, back_img)

            # 获取目标图像所在目录的相对路径
            src_dir_rel = os.path.relpath(os.path.dirname(src_img),
                                          start=os.getcwd())

            # 构建保存路径的相对路径
            file_path_rel = os.path.join(src_dir_rel, f'{name}.png')

            # 将相对路径转换为绝对路径，以便保存图像
            file_path_abs = os.path.abspath(file_path_rel)

            # 保存图像
            cv2.imwrite(file_path_abs, target_image)

            # 返回相对路径
            return file_path_rel
        except Exception as e:
            print(f"保存图像时发生错误: {e}")
            return ""

    @staticmethod
    def compare_image_v3(source_image_path, back_image_path, show=False):
        """
           检查给定的源图像与从背景图像中提取的目标图像是否相似。v2版本更加严格。

           参数:
               source_image_path (str): 源图像的文件路径。
               back_image_path (str): 背景图像的文件路径，从中将提取目标图像。
               show (bool, optional): 是否显示源图像和目标图像。默认为 False。

           返回:
               bool: 如果源图像和目标图像之间的相似度满足条件则返回 True，否则返回 False。

           抛出:
               ValueError: 当无法从指定路径读取图像时抛出。
               Exception: 当发生其他错误时抛出。
           """
        try:
            # 读取源图像和目标图像
            source_image = cv2.imread(source_image_path)
            target_image = ImageProcessor.capture_target_image_v1(source_image_path,
                                                   back_image_path)

            if source_image is None or target_image is None:
                raise ValueError("无法读取指定路径的图像")

            # 计算并归一化单通道直方图
            source_hist = cv2.calcHist([source_image], [0], None, [256], [0, 256])
            target_hist = cv2.calcHist([target_image], [0], None, [256], [0, 256])
            cv2.normalize(source_hist,
                          source_hist,
                          alpha=0,
                          beta=1,
                          norm_type=cv2.NORM_MINMAX)
            cv2.normalize(target_hist,
                          target_hist,
                          alpha=0,
                          beta=1,
                          norm_type=cv2.NORM_MINMAX)

            # 使用 OpenCV 内置的比较直方图函数
            single_channel_similarity = cv2.compareHist(source_hist, target_hist,
                                                        cv2.HISTCMP_CORREL)

            # 计算多通道直方图相似度
            resized_size = (256, 256)
            source_resized = cv2.resize(source_image, resized_size)
            target_resized = cv2.resize(target_image, resized_size)
            multi_channel_similarity = sum(
                cv2.compareHist(
                    cv2.calcHist([s_channel], [0], None, [256], [0, 256]),
                    cv2.calcHist([t_channel], [0], None, [256], [0, 256]),
                    cv2.HISTCMP_CORREL) for s_channel, t_channel in zip(
                        cv2.split(source_resized), cv2.split(target_resized))) / 3

            # 显示图片
            if show:
                # 打印结果
                print(f'多通道直方图相似度：{round(multi_channel_similarity, 2)}')
                print(f"单通道直方图相似度：{round(single_channel_similarity, 2)}")
                cv2.imshow("Source Image", source_image)
                cv2.imshow("Target Image", target_image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            # 返回判断结果
            return multi_channel_similarity > 0.5 and single_channel_similarity > 0.5

        except Exception as e:
            print(f"发生错误：{e}")
            return False

    @staticmethod
    def compare_image_colors(image_path1: str, image_path2: str, color: List[List[int]], threshold: float) -> bool:
        """比较两张图片中指定颜色区域的相似度
        
        Args:
            image_path1: 第一张图片路径
            image_path2: 第二张图片路径  
            color: HSV颜色范围
            threshold: 相似度阈值
            
        Returns:
            如果相似度大于阈值返回True,否则返回False
        """
        def process_image(image_path: str, color: List[List[int]], kernel: np.ndarray) -> float:
            try:
                image = cv2.imread(image_path)
                if image is None:
                    raise ValueError(f"无法读取图片: {image_path}")
                
                logger.debug(f"处理图片: {image_path}")
                hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                lower = np.array(color[0])
                upper = np.array(color[1])
                mask = cv2.inRange(hsv, lower, upper)
                blurred_mask = cv2.GaussianBlur(mask, (5, 5), 0)
                opening = cv2.morphologyEx(blurred_mask, cv2.MORPH_OPEN, kernel)
                closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
                contours, _ = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                
                if not contours:
                    logger.debug("未找到轮廓")
                    return 0
                    
                area = cv2.contourArea(max(contours, key=cv2.contourArea))
                logger.debug(f"计算区域面积: {area}")
                return area
                
            except Exception as e:
                logger.debug(f"图片处理失败: {e}")
                raise

        try:
            logger.debug("开始比较图片颜色")
            kernel = np.ones((5, 5), np.uint8)
            area1 = process_image(image_path1, color, kernel)
            area2 = process_image(image_path2, color, kernel)
            
            area_diff = abs(area1 - area2)
            max_area = max(area1, area2)
            similarity = 1 - (area_diff / max_area) if max_area > 0 else 0
            
            logger.debug(f"颜色相似度: {similarity}")
            return similarity >= threshold
            
        except Exception as e:
            logger.debug(f"比较图片颜色失败: {e}")
            return False

    @staticmethod
    def colors_exists(image_path, color_range, rate=0.2):
        """
        判断图片的主要颜色是否在给定的颜色范围内。

        :param image_path: 图片文件路径
        :param color_range: 颜色范围，格式为 [[H_min, S_min, V_min], [H_max, S_max, V_max]]
        :return: 如果主要颜色在范围内返回 True，否则返回 False
        """
        # 读取图片
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("无法读取图片，请检查路径是否正确")

        # 将图片从 BGR 转换为 HSV
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # 定义颜色范围
        lower_bound = np.array(color_range[0])
        upper_bound = np.array(color_range[1])

        # 创建掩码
        mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

        # 计算掩码中的像素数
        total_pixels = image.shape[0] * image.shape[1]
        masked_pixels = cv2.countNonZero(mask)
        print(f'颜色占比:{masked_pixels / total_pixels}')
        # 判断主要颜色是否在范围内
        if masked_pixels / total_pixels > rate:
            return True
        else:
            return False

    @staticmethod
    def crop_image_by_corners(image_input, corners):
        """
        根据四角坐标裁剪图片。

        参数:
            image_input (str or numpy.ndarray): 图片文件路径或已加载的OpenCV图像。
            corners (list of tuples): 四个角的坐标 [(x1, y1), (x2, y2), (x3, y3), (x4, x4)]。

        返回:
            numpy.ndarray: 裁剪后的图片。
        """
        try:
            # 检查输入是文件路径还是已加载的图像
            if isinstance(image_input, str):
                img = cv2.imread(image_input)
                if img is None:
                    raise ValueError("无法读取图片，请检查路径是否正确")
            elif isinstance(image_input, np.ndarray):
                img = image_input
            else:
                raise TypeError("image_input 必须是字符串路径或numpy.ndarray类型的图像")

            # 获取四角坐标
            x1, y1 = corners[0]
            x2, y2 = corners[1]
            x3, y3 = corners[2]
            x4, y4 = corners[3]

            # 计算裁剪区域的边界
            min_x = min(x1, x2, x3, x4)
            min_y = min(y1, y2, y3, y4)
            max_x = max(x1, x2, x3, x4)
            max_y = max(y1, y2, y3, y4)

            # 裁剪图片
            cropped_img = img[min_y:max_y, min_x:max_x]

            return cropped_img
        except Exception as e:
            logger.error(f"图像裁剪失败: {e}")
            return None


if __name__ == '__main__':
    # 定义图片目录
    IMG_DIR = r"C:\Users\admin\PycharmProjects\AFKJ_tool"
    # 定义具体路径
    back = fr"{IMG_DIR}\img/test/auto.png"
    # src = fr"{IMG_DIR}\img/test/auto1.png"
    src = fr"D:\temp\imgbao\screenshot.png"
    dir = fr"{IMG_DIR}\tt"
    # 获取四角坐标
    corners = [[556, 924], [740, 924], [740, 951], [556, 951]]
    img = ImageProcessor.crop_image_by_corners(src, corners)
    cv2.imshow("123123", img)
    cv2.waitKey(0)
    # -----------------------------------------------------------------
    # get_corners(src, back,1)
    # -----------------------------------------------------------------
    # get_center_location(src, back,1)
    # -----------------------------------------------------------------
    # capture_target_image_v1(src, back,1)
    # -----------------------------------------------------------------
    # xy =process_images(dir, back, 'center',1)
    # print(xy)
    # -----------------------------------------------------------------
    # color=[[0, 71, 78],[39, 255, 255]]
    # is_similar = compare_image_colors(back, src, color)
    # print(f"Images are {'similar' if is_similar else 'not similar'}")
    # -----------------------------------------------------------------

    # -----------------------------------------------------------------
    # 绿色
    # color=[[10, 0, 35], [85, 191, 213]]
    # reuslt = colors_exists(src, color)
    # print(reuslt)
