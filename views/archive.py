import os
import json
import pygame
import sys

from utils import config


def show_saves(screen, width, height, is_save):
    save_dir = config.save_dir
    # 存档文件列表
    save_files = [f"save_{i}.json" for i in range(1, 5)]
    save_data = []

    # 加载存档信息
    for file_name in save_files:
        file_path = os.path.join(save_dir, file_name)
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                try:
                    data = json.load(f)
                    save_data.append(data)
                except json.JSONDecodeError:
                    save_data.append({"is_empty": True})  # 防止解析错误
        else:
            save_data.append({"is_empty": True})  # 文件不存在则视为空存档

    # 字体设置
    font = pygame.font.Font(config.global_font, width // 20)
    selected_index = 0

    running = True
    while running:
        # 绘制背景和存档标题
        screen.fill((0, 0, 0))
        title = font.render(u'存档列表', True, (255, 255, 255))
        trect = title.get_rect(center=(width // 2, height // 10))
        screen.blit(title, trect)

        # 显示存档信息
        for i, data in enumerate(save_data):
            if data.get("is_empty", True):
                text = "空存档"
            else:
                level = data.get("level", "未知关卡")
                time_str = data.get("time", "未知时间")
                text = f"关卡: {level} | 时间: {time_str}"
            color = (0, 255, 0) if i == selected_index else (255, 255, 255)
            content = font.render(text, True, color)
            rect = content.get_rect(midtop=(width // 2, height // 5 + i * 50))
            screen.blit(content, rect)

        # 显示提示文字
        tip_text = "按 ESC 返回，回车确认" if is_save else "按 ESC 返回，回车读取"
        tip_surface = font.render(tip_text, True, (200, 200, 200))
        tip_rect = tip_surface.get_rect(center=(width // 2, height - 50))
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
                    if is_save:
                        return save_game(selected_file)  # 覆盖存档
                    else:
                        return load_game(selected_file)  # 读取存档
                elif event.key == pygame.K_ESCAPE:  # 返回主菜单
                    return None

def save_game(file_path):
    # """保存当前游戏状态到指定存档"""
    # game_data = {
    #     "is_empty": False,
    #     "level": current_level,  # 需要在主程序中提供 current_level
    #     "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # }
    # try:
    #     with open(file_path, "w") as f:
    #         json.dump(game_data, f)
    #     print(f"存档保存成功: {file_path}")
    # except IOError as e:
    #     print(f"存档保存失败: {e}")
    return "save_success"

def load_game(file_path):
    """加载游戏存档"""
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        print(f"存档加载成功: {file_path}")
        return data
    except FileNotFoundError:
        print("存档文件不存在！")
    except json.JSONDecodeError:
        print("存档文件解析错误！")
    return None
