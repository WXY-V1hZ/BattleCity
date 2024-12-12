import pygame, sys

global_font = "font/fusion-pixel-10px-monospaced-zh_hans.ttf"


# 显示菜单界面
def show_menu (screen, width, height):
    menu_font = pygame.font.Font(global_font, width // 10)
    menu_items = ['继续游戏', '退出游戏']
    selected_index = 0  # 当前选中的菜单项

    running = True
    while running:
        screen.fill((0, 0, 0))  # 清屏，背景为黑色

        # 绘制菜单项
        for i, item in enumerate(menu_items):
            color = (0, 255, 0) if i == selected_index else (255, 255, 255)  # 高亮选中的菜单项
            item_text = menu_font.render(item, True, color)
            rect = item_text.get_rect(center = (width // 2, height // 3 + i * 100))
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
                    if selected_index == 0:  # 选中“开始游戏”
                        return 'continue_game'
                    elif selected_index == 1:  # 选中“退出游戏”
                        return 'quit_game'
                elif event.key == pygame.K_ESCAPE:  # 按Esc键退出菜单
                    return 'exit_menu'

# 开始界面显示
def show_start(screen, width, height):
    tfont = pygame.font.Font(global_font, width // 5)
    cfont = pygame.font.Font(global_font, width // 20)

    while True:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                elif event.key == pygame.K_2:
                    return 2
                elif event.key == pygame.K_ESCAPE:
                    menu_result = show_menu(screen, 630, 630)
                    if menu_result == "exit_menu":
                        # 返回游戏继续进行
                        break
                    elif menu_result == "quit_game":
                        pygame.quit()
                        sys.exit()  # 退出游戏
                    else:
                        break

        # 清空屏幕并绘制内容
        screen.fill((0, 0, 0))  # 背景填充为黑色
        title = tfont.render(u'TANK', True, (255, 0, 0))
        content1 = cfont.render(u'1 PLAYER（按1）', True, (0, 0, 255))
        content2 = cfont.render(u'2 PLAYER（按2）', True, (0, 0, 255))
        trect = title.get_rect()
        trect.midtop = (width / 2, height / 5)
        crect1 = content1.get_rect()
        crect1.midtop = (width / 2, height / 1.8)
        crect2 = content2.get_rect()
        crect2.midtop = (width / 2, height / 1.6)
        screen.blit(title, trect)
        screen.blit(content1, crect1)
        screen.blit(content2, crect2)
        pygame.display.update()

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
        fail_img = pygame.image.load("images/others/gameover.png")
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
    bg_img = pygame.image.load("images/others/background.png")
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
