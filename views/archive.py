import os
import pickle
from datetime import datetime

import pygame
import sys
from utils import config
from entity.result import Result


def show_saves(screen, width, height, game_data_now=None):
    save_dir = config.save_dir
    # 存档文件列表
    save_files = [f"save_{i}.pickle" for i in range(1, 5)]
    save_data = []

    # 加载存档信息
    for file_name in save_files:
        file_path = os.path.join(save_dir, file_name)
        if os.path.exists(file_path):
            try:
                with open(file_path, "rb") as f:
                    data = pickle.load(f)
                    save_data.append(data)
            except Exception as e:
                print(f"加载存档出错, {e}")
                save_data.append({"is_empty": True})  # 防止解析错误
        else:
            save_data.append({"is_empty": True})  # 文件不存在则视为空存档

    # 字体设置
    font = pygame.font.Font(config.global_font, width // 30)
    selected_index = 0
    box_height = height // 6
    box_margin = 10
    box_width = width - 2 * box_margin

    running = True
    while running:
        screen.fill((0, 0, 0))  # 清屏

        # 绘制标题
        title_font = pygame.font.Font(config.global_font, width // 20)
        title = title_font.render(u'存档列表', True, (255, 255, 255))
        trect = title.get_rect(center=(width // 2, height // 12))
        screen.blit(title, trect)

        # 绘制每个存档框
        for i, data in enumerate(save_data):
            box_top = height // 5 + i * (box_height + box_margin)
            rect = pygame.Rect(box_margin, box_top, box_width, box_height)

            # 选中框高亮
            border_color = (0, 255, 0) if i == selected_index else (255, 255, 255)
            pygame.draw.rect(screen, border_color, rect, 3)

            # 填充存档内容
            if data.get("is_empty", False):
                text_lines = ["空存档"]
            else:
                stage = data.get("stage", "未知关卡")
                save_time = data.get("save_time", "未知时间")
                num_player = data.get("num_player", 1)
                mode = "双人模式" if num_player > 1 else "单人模式"
                text_lines = [
                    f"关卡: {stage}",
                    f"时间: {save_time}",
                    f"模式: {mode}"
                ]

            # 在框内显示多行文本
            for j, line in enumerate(text_lines):
                text_surface = font.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(
                    midleft=(box_margin + 10, box_top + 20 + j * 30)
                )
                screen.blit(text_surface, text_rect)

        # 显示提示文字
        tip_font = pygame.font.Font(config.global_font, width // 40)
        tip_text = "按 ESC 返回，回车确认" if game_data_now is not None else "按 ESC 返回，回车读取"
        tip_surface = tip_font.render(tip_text, True, (200, 200, 200))
        tip_rect = tip_surface.get_rect(center=(width // 2, height - 30))
        screen.blit(tip_surface, tip_rect)

        pygame.display.update()

        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(save_files)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(save_files)
                elif event.key == pygame.K_RETURN:  # 确认选择
                    selected_file = os.path.join(save_dir, save_files[selected_index])
                    if game_data_now is not None:
                        return save_game(selected_file, game_data_now)  # 保存存档
                    else:
                        return Result("load_game", load_game(selected_file))
                elif event.key == pygame.K_ESCAPE:  # 返回主菜单
                    return Result("back_to_home", None)

def save_game(file_path, game_data_now):
    """保存当前游戏状态到指定存档"""
    try:
        game_data_now["save_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(file_path, "wb") as f:
            pickle.dump(game_data_now, f)
        return "存档成功"
    except Exception as e:
        print(f"存档失败, {e}")
        return "存档失败"

def load_game(file_path):
    """加载游戏存档"""
    try:
        with open(file_path, "rb") as f:
            data = pickle.load(f)
        return data
    except:
        return None

