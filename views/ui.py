import pygame, sys
from PIL import Image, ImageFilter

global_font = "assets/font/fusion-pixel-10px-monospaced-zh_hans.ttf"


def apply_blur(surface, scale=4):
    """对传入的surface进行简单的模糊处理"""
    width, height = surface.get_size()
    small_surface = pygame.transform.smoothscale(surface, (width // scale, height // scale))
    return pygame.transform.smoothscale(small_surface, (width, height))

def apply_gaussian_blur(surface, radius=10):
    """使用 Pillow 对传入的 surface 进行高斯模糊"""
    # 将 Pygame 的 Surface 转换为 Pillow 的 Image
    raw_str = pygame.image.tostring(surface, "RGBA")
    pil_image = Image.frombytes("RGBA", surface.get_size(), raw_str)

    # 应用高斯模糊
    blurred_image = pil_image.filter(ImageFilter.GaussianBlur(radius))

    # 将处理后的 Pillow 图像转换回 Pygame 的 Surface
    return pygame.image.fromstring(blurred_image.tobytes(), surface.get_size(), "RGBA")

def show_menu(screen, width, height):
    menu_font = pygame.font.Font(global_font, width // 10)
    menu_items = ['继续游戏', '存档', '读档', '退出游戏']
    selected_index = 0  # 当前选中的菜单项

    # 捕获当前屏幕作为背景，并应用模糊效果
    background = screen.copy()
    blurred_background = apply_gaussian_blur(background, radius=15)

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
            rect = item_text.get_rect(center=(width // 2, start_y + i * item_height))
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
                    if selected_index == 0: return 'exit_menu'
                    elif selected_index == 1: return 'save_game'
                    elif selected_index == 2: return 'load_game'
                    elif selected_index == 3: return 'quit_game'
                else:  # 按Esc键退出菜单
                    return 'exit_menu'

def show_start(screen, width, height):
    tfont = pygame.font.Font(global_font, width // 5)
    cfont = pygame.font.Font(global_font, width // 20)

    start_items = ['单人模式', '双人模式', '退出游戏']  # 开始界面选项
    selected_index = 0  # 当前选中的选项

    running = True
    while running:
        # 清空屏幕并绘制标题
        screen.fill((0, 0, 0))  # 背景填充为黑色
        title = tfont.render(u'坦克大战', True, (255, 0, 0))
        trect = title.get_rect()
        trect.midtop = (width / 2, height / 5)
        screen.blit(title, trect)

        # 绘制选项
        for i, item in enumerate(start_items):
            color = (0, 255, 0) if i == selected_index else (0, 0, 255)  # 高亮选中项
            content = cfont.render(f'{item}', True, color)
            rect = content.get_rect()
            rect.midtop = (width / 2, height / 1.8 + i * 50)
            screen.blit(content, rect)

        pygame.display.update()  # 更新屏幕

        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # 按上箭头
                    selected_index = (selected_index - 1) % len(start_items)
                elif event.key == pygame.K_DOWN:  # 按下箭头
                    selected_index = (selected_index + 1) % len(start_items)
                elif event.key == pygame.K_RETURN:  # 按回车键确认
                    if   selected_index == 0: return 1
                    elif selected_index == 1: return 2
                    elif selected_index == 2: # 选中“退出游戏”
                        pygame.quit()
                        sys.exit()  # 退出游戏
                elif event.key == pygame.K_ESCAPE:  # 按ESC键进入菜单
                    menu_result = show_menu(screen, width, height)
                    if menu_result == "exit_menu": break
                    elif menu_result == "quit_game":
                        pygame.quit()
                        sys.exit()
                    # elif menu_result == "save_game":
                    #     save_game()
                    # elif menu_result == "load_game":
                    #     load_game()
                    else: break


# 结束界面显示
def show_end (screen, width, height, is_win):
    bg_img = pygame.image.load("images/others/background.png")
    screen.blit(bg_img, (0, 0))
    if is_win:
        font = pygame.font.Font(global_font, width // 10)
        content = font.render(u'恭喜通关！', True, (255, 0, 0))
        rect = content.get_rect()
        rect.midtop = (width / 2, height / 2)
        screen.blit(content, rect)
    else:
        fail_img = pygame.image.load("assets/images/others/gameover.png")
        rect = fail_img.get_rect()
        rect.midtop = (width / 2, height / 2)
        screen.blit(fail_img, rect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

# 关卡切换界面
def show_switch_stage(screen, width, height, stage):
    bg_img = pygame.image.load("assets/images/others/background.png")
    screen.blit(bg_img, (0, 0))
    font = pygame.font.Font(global_font, width // 10)
    content = font.render(u'第%d关' % stage, True, (0, 255, 0))
    rect = content.get_rect()
    rect.midtop = (width / 2, height / 2)
    screen.blit(content, rect)
    pygame.display.update()

    delay_event = pygame.constants.USEREVENT
    pygame.time.set_timer(delay_event, 1000)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == delay_event:
                pygame.time.set_timer(delay_event, 0)  # 停止定时器
                return
