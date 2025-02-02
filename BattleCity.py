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
        # 监测按键
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 当前状态为开始
        if current_state == "start":
            start_result = ui.show_start(screen, width, height)
            if start_result.msg == "num_player":
                num_player = start_result.data
            elif start_result.msg == "load_game":
                game_data = start_result.data
                if game_data is not None:
                    stage = game_data["stage"]
                    num_player = game_data["num_player"]
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

            if game_result.msg == "back_to_start":
                current_state = "start"
                game_data = None
                stage = 0
                continue
            elif game_result.msg == "load_game":
                game_data = game_result.data
                stage = game_data["stage"]
                num_player = game_data["num_player"]
                continue

            # 通关
            if stage >= num_stage:
                is_win = True
                current_state = "end"
            # 失败
            if game_result.msg == 'lose':
                is_win = False
                current_state = "end"

            game_data = None
        # 当前状态为结束
        elif current_state == "end":
            stage = 0
            game_data = None

            # 根据是否失败显示胜败界面
            end_result = ui.show_end(screen, width, height, is_win)

            if end_result == 'back_to_start':
                current_state = "start"
            else:
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    main()
