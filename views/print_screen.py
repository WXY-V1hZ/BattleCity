import pygame

from utils import tools


def show(screen, width, height):
    """显示截屏动画"""
    overlay_color = (0, 0, 0, 128)  # 半透明黑色
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill(overlay_color)

    # 显示短暂的闪烁效果
    for _ in range(3):
        screen.blit(overlay, (0, 0))
        pygame.display.update()
        pygame.time.delay(50)  # 持续 50ms
        screen.fill((0, 0, 0))  # 清除覆盖层
        pygame.display.update()
        pygame.time.delay(50)

def listen(screen, width, height, event):
    if event.mod & pygame.KMOD_CTRL and event.key == pygame.K_p:
        tools.print_screen(screen)
        show(screen, width, height)
