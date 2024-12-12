import sys

import pygame

from entity import home, scene, tank, food
from entity.resources import Resources
from views import ui, menu

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
            num_player = ui.show_start(screen, width, height)
            current_state = "playing"
        # 当前状态为游玩中
        elif current_state == "playing":
            # 关卡递增
            stage += 1

            # 显示关卡界面
            ui.show_switch_stage(screen, width, width, stage)
            # 播放开始音乐
            resources.start_sound.play()

            # 进入游戏
            game_result = ui.show_game(screen, width, height, num_player, stage, clock, resources)

            # 通关
            if stage == num_stage:
                is_win = True
                current_state = "end"
            # 失败
            if game_result == 'lose':
                is_win = False
                current_state = "end"
        # 当前状态为结束
        elif current_state == "end":
            # 根据是否失败显示胜败界面
            ui.show_end(screen, width, height, is_win)

if __name__ == '__main__':
    main()
