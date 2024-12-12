import pygame, sys
from PIL import Image, ImageFilter

from utils import archive, config
from views import ui

def apply_gaussian_blur(surface, radius=10):
    """使用 Pillow 对传入的 surface 进行高斯模糊"""
    # 将 Pygame 的 Surface 转换为 Pillow 的 Image
    raw_str = pygame.image.tostring(surface, "RGBA")
    pil_image = Image.frombytes("RGBA", surface.get_size(), raw_str)

    # 应用高斯模糊
    blurred_image = pil_image.filter(ImageFilter.GaussianBlur(radius))

    # 将处理后的 Pillow 图像转换回 Pygame 的 Surface
    return pygame.image.fromstring(blurred_image.tobytes(), surface.get_size(), "RGBA")

def show(screen, width, height):
    menu_font = pygame.font.Font(config.global_font, width // 10)
    menu_items = ['继续游戏', '存档', '读档', '返回主页', '退出游戏']
    selected_index = 0  # 当前选中的菜单项

    # 捕获当前屏幕作为背景，并应用模糊效果
    background = screen.copy()
    blurred_background = apply_gaussian_blur(background, radius = 15)

    item_height = 100  # 每个选项的垂直间距
    menu_height = item_height * len(menu_items)  # 菜单总高度
    start_y = (height - menu_height) // 2  # 起始绘制的Y坐标，确保菜单居中

    running = True
    while running:
        screen.blit(blurred_background, (0, 0))  # 绘制模糊背景

        # 绘制菜单项
        for i, item in enumerate(menu_items):
            color = (0, 255, 0) if i == selected_index else (255, 255, 255)  # 高亮选中的菜单项
            item_text = menu_font.render(item, True, color)
            rect = item_text.get_rect(center = (width // 2, start_y + i * item_height))
            screen.blit(item_text, rect)

        pygame.display.update()  # 更新屏幕

        # 事件监听
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # 按上箭头
                    selected_index = (selected_index - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:  # 按下箭头
                    selected_index = (selected_index + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:  # 按回车键确认
                    if selected_index == 0:
                        return 'exit_menu'
                    elif selected_index == 1:
                        return 'save_game'
                    elif selected_index == 2:
                        return 'load_game'
                    elif selected_index == 3:
                        return 'back_to_title'
                    elif selected_index == 4:
                        return 'quit_game'
                else:  # 按Esc键退出菜单
                    return 'exit_menu'

def listen(screen, width, height, event):
    if event.key == pygame.K_ESCAPE:  # 按ESC键进入菜单
        menu_result = show(screen, width, height)
        if menu_result == "exit_menu":
            return 0
        elif menu_result == "quit_game":
            pygame.quit()
            sys.exit()
        elif menu_result == "save_game":
            archive.save_game()
        elif menu_result == "load_game":
            archive.load_game()
        elif menu_result == "back_to_title":
            pass
        else:
            return 0