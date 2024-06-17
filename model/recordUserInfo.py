import yaml
from PIL import Image
from model.loadUserDataBase import get_db_connection
import numpy as np
import cv2


class InfoRecord:
    def __init__(self, username, rowimage, processedimage):
        # 连接到数据库
        self.user_images_db = get_db_connection()
        self.cursor = self.user_images_db.cursor()

        # 从YAML配置文件中读取图片保存路径
        with open('config/route.yaml', 'r') as file:
            config = yaml.safe_load(file)
            self.img_pth = config['database_settings']['row_img_save_pth']  # 保存原始图片
            self.processed_img_pth = config['database_settings']['processed_img_save_pth']  # 保存处理后的图片

        # 构造文件名并分别保存原始图片和处理后的图片
        rowimg_filename = f"{username}_original.jpg"
        procimg_filename = f"{username}_processed.jpg"


        filename_row = f"{username}row.jpg"  # 简化文件命名，假设每次处理都会覆盖旧文件或有其他机制管理文件版本
        filename_pro= f"{username}processed.jpg"
        self.path = self.save_image_to_disk(rowimage, self.img_pth, filename_row)
        self.path = self.save_image_to_disk(processedimage, self.processed_img_pth, filename_pro)

        # 更新数据库中的图像计数
        self.update_user_image_count(username)

    def save_image_to_disk(self, image, base_path, filename):
        """
        保存图片到指定路径。
        支持NumPy数组和PIL Image对象，确保保存为RGB格式。
        """
        path = base_path + filename

        # 如果输入是NumPy数组，检查并转换BGR到RGB
        if isinstance(image, np.ndarray):
            # 检查是否为三通道图像，通常表示BGR或RGB
            if len(image.shape) == 3 and image.shape[2] == 3:
                # 从BGR转换到RGB
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)

        # 确保PIL.Image对象也是RGB格式
        elif isinstance(image, Image.Image) and 'mode' in image.info and image.mode != 'RGB':
            image = image.convert('RGB')

        # 现在可以安全地保存图像
        image.save(path)

        return path


    def update_user_image_count(self, username):
        """
        更新用户在数据库中的已处理图像数量。
        """
        with self.user_images_db.cursor() as cursor:
            cursor.execute("""
                UPDATE `users` 
                SET 
                    `processed_images_count` = `processed_images_count` + 1, 
                    `original_images_count` = `original_images_count` + 1
                WHERE `id` = %s
            """, (username,))
        # 修改这里，使用数据库连接进行提交
        self.user_images_db.commit()

    def record_images_info(self, username, original_image_url, processed_image_url):
        """
        记录用户原始和处理过的图像信息到数据库。
        """
        # 检查用户是否存在，如果不存在则插入新记录
        with self.user_images_db.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) FROM `userinfo` WHERE `user_id` = %s
            """, (username,))
            user_exists = cursor.fetchone()[0]

        if not user_exists:
            with self.user_images_db.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO `userinfo`  
                    (`user_id`, `original_image_url`, `processed_image_url`) 
                    VALUES (%s, %s, %s)
                """, (username, original_image_url, processed_image_url))
        else:
            with self.user_images_db.cursor() as cursor:
                cursor.execute("""
                    UPDATE `userinfo` 
                    SET 
                        `original_image_url` = %s, 
                        `processed_image_url` = %s
                    WHERE `user_id` = %s
                """, (original_image_url, processed_image_url, username))
        self.cursor.commit()
