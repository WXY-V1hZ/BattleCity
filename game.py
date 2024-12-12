import sys

import pygame

from entity.resources import Resources
from views import ui


# 主函数
def main ():
    # 初始化
    pygame.init()
    pygame.mixer.init()

    width = 630
    height = 630
    num_player = 0
    stage = 0
    num_stage = 2
    is_win = True
    game_data = None
    clock = pygame.time.Clock()
    current_state = "start"

    resources = Resources.get_instance()

    # 设置窗口大小
    screen = pygame.display.set_mode((width, height))
    # 设置窗口标题
    pygame.display.set_caption("坦克大战")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 当前状态为开始
        if current_state == "start":
            start_result = ui.show_start(screen, width, height)
            if isinstance(start_result, int):
                num_player = start_result
            else:
                game_data = start_result
            current_state = "game"
        # 当前状态为游玩中
        elif current_state == "game":
            # 不需要加载存档
            if not game_data:
                stage += 1
                # 播放开始音乐
                if stage == 1: resources.start_sound.play()
                # 显示关卡切换界面
                ui.show_switch_stage(screen, width, width, stage)

            # 进入游戏
            game_result = ui.show_game(screen, width, height, num_player, stage, clock, game_data)

            if game_result == "back_to_start":
                current_state = "start"
                stage = 0
                continue
            elif isinstance(game_result, dict):
                game_data = game_result
                continue

            # 通关
            if stage == num_stage:
                is_win = True
                current_state = "end"
            # 失败
            if game_result == 'lose':
                is_win = False
                current_state = "end"

            game_data = None
        # 当前状态为结束
        elif current_state == "end":
            stage = 0

            # 根据是否失败显示胜败界面
            end_result = ui.show_end(screen, width, height, is_win)

            if end_result == 'back_to_start':
                current_state = "start"
            else:
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    main()
