from datetime import datetime

import pygame, os

from utils import config


def print_screen(screen):
    """保存当前屏幕为图片"""
    if not os.path.exists(config.screenshot_dir):
        os.makedirs(config.screenshot_dir)

    # 基于时间戳生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(config.screenshot_dir, f"screenshot_{timestamp}.png")

    # 保存屏幕内容
    pygame.image.save(screen, file_path)