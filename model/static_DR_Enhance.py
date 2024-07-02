import cv2
import numpy as np


class ImageEnhancer:
    def __init__(self, image):
        self.image=image

    def otsu_thresholding(self, image):
        blur = cv2.GaussianBlur(image, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresh

    def artificial_fish_swarm_otsu(self, image):
        # 使用人工鱼群算法优化Otsu阈值 (简单模拟)
        return self.otsu_thresholding(image)

    def histogram_equalization(self, image):
        return cv2.equalizeHist(image)

    def nonlinear_enhancement(self, image):
        gamma = 1.2  # 调整gamma值以减少增强过度
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        return cv2.LUT(image, table)

    def enhance_image(self):
        # 在转换之前，添加详细的检查
        if self.image is None or self.image.size == 0:
            raise ValueError("Image data is empty.")
        if self.image.ndim != 3 or self.image.shape[-1] != 3:
            raise ValueError("Invalid image format, expecting a 3-channel BGR image.")

        print(f"Image shape before conversion: {self.image.shape}")

        try:
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        except cv2.error as e:
            print(f"Error during color conversion: {e}")
            raise

        # 阈值分割
        segmented = self.artificial_fish_swarm_otsu(gray)

        # 分解图像
        high_freq_strong = cv2.bitwise_and(gray, gray, mask=segmented)
        high_freq_weak_and_low_freq = cv2.bitwise_and(gray, gray, mask=cv2.bitwise_not(segmented))

        # 图像增强
        enhanced_high_freq_strong = self.nonlinear_enhancement(high_freq_strong)
        enhanced_high_freq_weak_and_low_freq = self.histogram_equalization(high_freq_weak_and_low_freq)

        # 将增强后的部分组合在一起
        enhanced_image = cv2.addWeighted(enhanced_high_freq_strong, 1, enhanced_high_freq_weak_and_low_freq, 1, 0)

        # 中值滤波以去噪
        denoised_enhanced_image = cv2.medianBlur(enhanced_image, ksize=3)

        return denoised_enhanced_image

# 使用方式
#image_enhancer = ImageEnhancer('img.png')
#enhanced_image = image_enhancer.enhance_image()

# 若要保存增强后的图像
# cv2.imwrite('enhanced_img.png', enhanced_image)
