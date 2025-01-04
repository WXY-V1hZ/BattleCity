import pygame, sys

from entity import home, scene, tank, food
from entity.resources import Resources
from entity.result import Result
from . import menu, print_screen
from utils import config
import time

from . import archive

# 显示开始界面
def show_start(screen, width, height):
    resources = Resources.get_instance()
    resources.bg_img = pygame.transform.scale(resources.bg_img, (width, height))  # 缩放背景图片
    tfont = pygame.font.Font(config.global_font, width // 5)
    cfont = pygame.font.Font(config.global_font, width // 20)

    start_items = ['单人模式', '双人模式', '读取存档', '退出游戏']  # 开始界面选项
    selected_index = 0  # 当前选中的选项

    running = True
    while running:
        # 清空屏幕并绘制标题
        screen.blit(resources.bg_img, (0, 0))
        title = tfont.render(u'坦克大战', True, (255, 0, 0))
        trect = title.get_rect()
        trect.midtop = (width / 2, height / 5)
        screen.blit(title, trect)

        # 绘制选项
        for i, item in enumerate(start_items):
            color = (0, 255, 0) if i == selected_index else (255, 255, 255)  # 高亮选中项
            content = cfont.render(f'{item}', True, color)
            rect = content.get_rect()
            rect.midtop = (width / 2, height / 1.8 + i * 50)
            screen.blit(content, rect)

        pygame.display.update() # 更新屏幕

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
                    if   selected_index == 0: return Result("num_player", 1)
                    elif selected_index == 1: return Result("num_player", 2)
                    elif selected_index == 2: # 读档
                        saves_result = archive.show_saves(screen, width, height)
                        if saves_result.msg == "back_to_home": continue
                        return saves_result
                    else:
                        pygame.quit()
                        sys.exit()

# 显示过渡动画
def transition_animation (screen, width, height, is_win):
    """过渡动画效果：截取最后的画面并逐渐覆盖，胜利为白色，失败为红色"""
    # 胜利和失败的颜色设置
    overlay_color = (255, 255, 255) if is_win else (255, 0, 0)  # 胜利为白色，失败为红色
    max_alpha = 128  # 最大透明度值（可以根据需求调整）
    transition_duration = 1.0  # 过渡持续时间（秒）
    transition_frames = 60  # 动画帧数（60帧，假设每帧大约1/60秒）

    # 初始背景填充
    screen.fill((0, 0, 0))
    pygame.display.update()

    for frame in range(transition_frames):
        # 计算每一帧的透明度（从0到最大透明度）
        overlay_alpha = int((max_alpha * frame) / transition_frames)

        # 在原画面上叠加一个透明的颜色层
        overlay_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay_surface.fill((overlay_color[0], overlay_color[1], overlay_color[2], overlay_alpha))

        screen.blit(overlay_surface, (0, 0))
        pygame.display.update()

        time.sleep(transition_duration / transition_frames)  # 每帧间隔时间

# 显示结束界面
def show_end(screen, width, height, is_win):
    # 获取资源
    resources = Resources.get_instance()

    transition_animation(screen, width, height, is_win)

    # 设置字体
    tfont = pygame.font.Font(config.global_font, width // 10)  # 大标题字体
    cfont = pygame.font.Font(config.global_font, width // 20)  # 选项字体

    # 选项内容
    end_items = ['返回主页', '退出游戏']
    selected_index = 0  # 当前选中的选项

    running = True
    while running:
        # 清空屏幕并绘制背景
        screen.blit(resources.bg_img, (0, 0))  # 背景图

        # 绘制胜利或失败信息
        if is_win:
            content = tfont.render(u'恭喜通关！', True, (0, 255, 0))  # 胜利时的文字
        else:
            content = tfont.render(u'游戏失败', True, (255, 0, 0))  # 失败时的文字

        rect = content.get_rect()
        rect.midtop = (width / 2, height / 5)  # 定位文本
        screen.blit(content, rect)

        # 绘制选项
        for i, item in enumerate(end_items):
            color = (0, 255, 0) if i == selected_index else (255, 255, 255)  # 高亮选中项
            content = cfont.render(f'{item}', True, color)
            rect = content.get_rect()
            rect.midtop = (width / 2, height / 1.8 + i * 50)  # 定位选项
            screen.blit(content, rect)

        pygame.display.update()  # 更新屏幕

        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # 按上箭头
                    selected_index = (selected_index - 1) % len(end_items)
                elif event.key == pygame.K_DOWN:  # 按下箭头
                    selected_index = (selected_index + 1) % len(end_items)
                elif event.key == pygame.K_RETURN:  # 按回车键确认
                    if selected_index == 0: # 回到主页
                        return "back_to_start"
                    elif selected_index == 1: # 退出游戏
                        pygame.quit()
                        sys.exit()
                    else:
                        pygame.quit()
                        sys.exit()

                    # 关卡切换界面

# 显示关卡切换界面
def show_switch_stage(screen, width, height, stage):
    # 获取资源
    resources = Resources.get_instance()

    screen.fill((0, 0, 0))  # 背景填充为黑色
    font = pygame.font.Font(config.global_font, width // 10)
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

# 显示游戏界面
def show_game(screen, width, height, num_player, stage, clock, game_data):
    # 获取资源
    resources = Resources.get_instance()

    # 该关卡坦克总数量
    enemytanks_total = min(stage * 12, 60)
    # 场上存在的敌方坦克总数量
    enemytanks_now = 0
    # 场上可以存在的敌方坦克总数量
    enemytanks_now_max = min(max(stage * 2, 4), 8)

    # 精灵组
    tanksGroup = pygame.sprite.Group()
    mytanksGroup = pygame.sprite.Group()
    enemytanksGroup = pygame.sprite.Group()
    enemybulletsGroup = pygame.sprite.Group()
    myfoodsGroup = pygame.sprite.Group()

    # 自定义事件
    # 	-生成敌方坦克事件
    genEnemyEvent = pygame.constants.USEREVENT + 0
    pygame.time.set_timer(genEnemyEvent, 100)
    # 	-敌方坦克静止恢复事件
    recoverEnemyEvent = pygame.constants.USEREVENT + 1
    pygame.time.set_timer(recoverEnemyEvent, 8000)
    # 	-我方坦克无敌恢复事件
    noprotectMytankEvent = pygame.constants.USEREVENT + 2
    pygame.time.set_timer(noprotectMytankEvent, 8000)

    # 资源初始化
    # 关卡地图
    # TODO: 地图编辑器
    map_stage = scene.Map(stage)
    # 我方坦克 TODO: 重构坦克类
    tank_player1 = tank.myTank(1)
    tanksGroup.add(tank_player1)
    mytanksGroup.add(tank_player1)
    if num_player > 1:
        tank_player2 = tank.myTank(2)
        tanksGroup.add(tank_player2)
        mytanksGroup.add(tank_player2)

    # 状态初始化
    is_switch_tank = True
    player1_moving = False
    player2_moving = False
    # 为了轮胎的动画效果
    time = 0

    # 敌方坦克，最多三辆
    for i in range(0, 3):
        if enemytanks_total > 0:
            enemytank = tank.enemyTank(i)
            tanksGroup.add(enemytank)
            enemytanksGroup.add(enemytank)
            enemytanks_now += 1
            enemytanks_total -= 1

    # 大本营
    myhome = home.Home()

    # 加载出场特效，根据图像大小提取帧
    appearance_img = pygame.image.load("assets/images/others/appear.png").convert_alpha()
    appearances = []
    appearances.append(appearance_img.subsurface((0, 0), (48, 48)))
    appearances.append(appearance_img.subsurface((48, 0), (48, 48)))
    appearances.append(appearance_img.subsurface((96, 0), (48, 48)))

    if game_data:  # 如果游戏数据存在，加载数据
        # 加载全局状态
        stage               = game_data.get("stage")
        enemytanks_total    = game_data.get("enemytanks_total")
        enemytanks_now      = game_data.get("enemytanks_now")
        enemytanks_now_max  = game_data.get("enemytanks_now_max")
        is_switch_tank      = game_data.get("is_switch_tank")
        player1_moving      = game_data.get("player1_moving")
        player2_moving      = game_data.get("player2_moving")
        time                = game_data.get("time", time)

        # tanksGroup = pygame.sprite.Group(game_data.get("tanksGroup", []))
        # mytanksGroup = pygame.sprite.Group(game_data.get("mytanksGroup", []))
        # enemytanksGroup = pygame.sprite.Group(game_data.get("enemytanksGroup", []))
        # 未能实现的:
        # 恢复角色、物品
        # 恢复地图
        # 恢复大本营

    game_data_now = {
        "stage"             : stage,
        "num_player"        : num_player,
        "enemytanks_total"  : enemytanks_total,
        "enemytanks_now"    : enemytanks_now,
        "enemytanks_now_max": enemytanks_now_max,
        "is_switch_tank"    : is_switch_tank,
        "player1_moving"    : player1_moving,
        "player2_moving"    : player2_moving,
        "time"              : time,

        # "tanksGroup"     : list(tanksGroup),
        # "mytanksGroup"   : list(mytanksGroup),
        # "enemytanksGroup": list(enemytanksGroup),
        # "map_stage"      : map_stage.export_state(),
        # "myhome"         : myhome.export_state()
    }

    # 关卡主循环
    while True:
        # 胜利
        if enemytanks_total < 1 and enemytanks_now < 1:
            return Result("win", None)

        # 事件监测
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                print_screen.listen(screen, width, height, event)

                menu_result = menu.listen(screen, width, height, event, game_data_now)
                if menu_result is not None and (menu_result.msg == "back_to_start" or menu_result.msg == "load_game"):
                    return menu_result


            # 增加坦克事件，检验是否还有敌方坦克 且 场上是否还能增加坦克
            if event.type == genEnemyEvent and enemytanks_total > 0 and enemytanks_now < enemytanks_now_max:
                enemytank = tank.enemyTank()
                # 检验生成位置是否与其他坦克重叠
                if pygame.sprite.spritecollide(enemytank, tanksGroup, False, None):
                    continue
                tanksGroup.add(enemytank)
                enemytanksGroup.add(enemytank)
                enemytanks_now += 1
                enemytanks_total -= 1

            # 恢复坦克的禁锢状态
            if event.type == recoverEnemyEvent:
                for each in enemytanksGroup:
                    each.can_move = True

            # 移除我方坦克的无敌状态
            if event.type == noprotectMytankEvent:
                for each in mytanksGroup:
                    mytanksGroup.protected = False

        # 检查用户键盘操作
        key_pressed = pygame.key.get_pressed()

        # 玩家一
        if num_player > 0:
            if key_pressed[pygame.K_w]:
                tanksGroup.remove(tank_player1)
                tank_player1.move_up(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
                tanksGroup.add(tank_player1)
                player1_moving = True
            elif key_pressed[pygame.K_s]:
                tanksGroup.remove(tank_player1)
                tank_player1.move_down(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
                tanksGroup.add(tank_player1)
                player1_moving = True
            elif key_pressed[pygame.K_a]:
                tanksGroup.remove(tank_player1)
                tank_player1.move_left(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
                tanksGroup.add(tank_player1)
                player1_moving = True
            elif key_pressed[pygame.K_d]:
                tanksGroup.remove(tank_player1)
                tank_player1.move_right(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
                tanksGroup.add(tank_player1)
                player1_moving = True
            elif key_pressed[pygame.K_j]:
                if not tank_player1.bullet.being:
                    resources.fire_sound.play()
                    tank_player1.shoot()
        # 玩家二
        if num_player > 1:
            if key_pressed[pygame.K_UP]:
                tanksGroup.remove(tank_player2)
                tank_player2.move_up(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
                tanksGroup.add(tank_player2)
                player2_moving = True
            elif key_pressed[pygame.K_DOWN]:
                tanksGroup.remove(tank_player2)
                tank_player2.move_down(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
                tanksGroup.add(tank_player2)
                player2_moving = True
            elif key_pressed[pygame.K_LEFT]:
                tanksGroup.remove(tank_player2)
                tank_player2.move_left(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
                tanksGroup.add(tank_player2)
                player2_moving = True
            elif key_pressed[pygame.K_RIGHT]:
                tanksGroup.remove(tank_player2)
                tank_player2.move_right(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
                tanksGroup.add(tank_player2)
                player2_moving = True
            elif key_pressed[pygame.K_0]:
                if not tank_player2.bullet.being:
                    resources.fire_sound.play()
                    tank_player2.shoot()

        # 绘制背景 TODO: 地图修改
        screen.fill((0, 0, 0))  # 背景填充为黑色
        # 石头墙
        for each in map_stage.brickGroup:
            screen.blit(each.brick, each.rect)
        # 钢墙
        for each in map_stage.ironGroup:
            screen.blit(each.iron, each.rect)
        # 冰
        for each in map_stage.iceGroup:
            screen.blit(each.ice, each.rect)
        # 河流
        for each in map_stage.riverGroup:
            screen.blit(each.river, each.rect)
        # 树
        for each in map_stage.treeGroup:
            screen.blit(each.tree, each.rect)

        time += 1
        if time == 5:
            time = 0
            is_switch_tank = not is_switch_tank

        # 我方坦克，玩家1
        if tank_player1 in mytanksGroup:
            if is_switch_tank and player1_moving:
                screen.blit(tank_player1.tank_0, (tank_player1.rect.left, tank_player1.rect.top))
                player1_moving = False
            else:
                screen.blit(tank_player1.tank_1, (tank_player1.rect.left, tank_player1.rect.top))
            if tank_player1.protected:
                screen.blit(tank_player1.protected_mask1, (tank_player1.rect.left, tank_player1.rect.top))
        # 玩家2
        if num_player > 1:
            if tank_player2 in mytanksGroup:
                if is_switch_tank and player2_moving:
                    screen.blit(tank_player2.tank_0, (tank_player2.rect.left, tank_player2.rect.top))
                    player1_moving = False
                else:
                    screen.blit(tank_player2.tank_1, (tank_player2.rect.left, tank_player2.rect.top))
                if tank_player2.protected:
                    screen.blit(tank_player1.protected_mask1, (tank_player2.rect.left, tank_player2.rect.top))

        # 敌方坦克
        for each in enemytanksGroup:
            # 出生特效
            if each.born:
                if each.times > 0:
                    each.times -= 1
                    if each.times <= 10:
                        screen.blit(appearances[2], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 20:
                        screen.blit(appearances[1], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 30:
                        screen.blit(appearances[0], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 40:
                        screen.blit(appearances[2], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 50:
                        screen.blit(appearances[1], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 60:
                        screen.blit(appearances[0], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 70:
                        screen.blit(appearances[2], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 80:
                        screen.blit(appearances[1], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 90:
                        screen.blit(appearances[0], (3 + each.x * 12 * 24, 3))
                else:
                    each.born = False
            else:
                if is_switch_tank:
                    screen.blit(each.tank_0, (each.rect.left, each.rect.top))
                else:
                    screen.blit(each.tank_1, (each.rect.left, each.rect.top))
                if each.can_move:
                    tanksGroup.remove(each)
                    each.move(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
                    tanksGroup.add(each)

        # 我方子弹 TODO：重构子弹类
        for tank_player in mytanksGroup:
            # 子弹不存在，跳过
            if not tank_player.bullet.being:
                continue

            # 子弹运动
            tank_player.bullet.move()
            screen.blit(tank_player.bullet.bullet, tank_player.bullet.rect)

            # 子弹碰撞敌方子弹
            for each in enemybulletsGroup:
                # 敌方子弹不存在，跳过
                if not each.being:
                    enemybulletsGroup.remove(each)
                    continue

                # 没有碰撞
                if not pygame.sprite.collide_rect(tank_player.bullet, each):
                    continue

                # 碰撞
                tank_player.bullet.being = False
                each.being = False
                enemybulletsGroup.remove(each)
                break

            # 子弹碰撞敌方坦克
            for each in enemytanksGroup:
                # 敌方坦克不存在，跳过
                if not each.being:
                    enemytanksGroup.remove(each)
                    tanksGroup.remove(each)
                    continue

                # 没有碰撞
                if not pygame.sprite.collide_rect(tank_player.bullet, each):
                    continue

                # 碰撞
                if each.is_red == True:
                    myfood = food.Food()
                    myfood.generate()
                    myfoodsGroup.add(myfood)
                    each.is_red = False
                each.blood -= 1
                each.color -= 1
                if each.blood < 0:
                    resources.bang_sound.play()
                    each.being = False
                    enemytanksGroup.remove(each)
                    enemytanks_now -= 1
                    tanksGroup.remove(each)
                else:
                    each.reload()
                tank_player.bullet.being = False
                break

            # 子弹碰撞石头墙
            if pygame.sprite.spritecollide(tank_player.bullet, map_stage.brickGroup, True, None):
                tank_player.bullet.being = False

            # 子弹碰钢墙
            if tank_player.bullet.stronger:
                if pygame.sprite.spritecollide(tank_player.bullet, map_stage.ironGroup, True, None):
                    tank_player.bullet.being = False
            else:
                if pygame.sprite.spritecollide(tank_player.bullet, map_stage.ironGroup, False, None):
                    tank_player.bullet.being = False

            # 子弹碰大本营
            if pygame.sprite.collide_rect(tank_player.bullet, myhome):
                tank_player.bullet.being = False
                myhome.set_dead()
                return Result("lose", None)

        # 敌方子弹
        for each in enemytanksGroup:
            if each.being:
                if each.can_move and not each.bullet.being:
                    enemybulletsGroup.remove(each.bullet)
                    each.shoot()
                    enemybulletsGroup.add(each.bullet)
                if not each.born:
                    if each.bullet.being:
                        each.bullet.move()
                        screen.blit(each.bullet.bullet, each.bullet.rect)
                        # 子弹碰撞我方坦克
                        for tank_player in mytanksGroup:
                            if pygame.sprite.collide_rect(each.bullet, tank_player):
                                if not tank_player.protected:
                                    resources.bang_sound.play()
                                    tank_player.life -= 1
                                    if tank_player.life < 0:
                                        mytanksGroup.remove(tank_player)
                                        tanksGroup.remove(tank_player)
                                        if len(mytanksGroup) < 1:
                                            return Result("lose", None)
                                    else:
                                        tank_player.reset()
                                each.bullet.being = False
                                enemybulletsGroup.remove(each.bullet)
                                break
                        # 子弹碰撞石头墙
                        if pygame.sprite.spritecollide(each.bullet, map_stage.brickGroup, True, None):
                            each.bullet.being = False
                            enemybulletsGroup.remove(each.bullet)

                        # 子弹碰钢墙
                        if each.bullet.stronger:
                            if pygame.sprite.spritecollide(each.bullet, map_stage.ironGroup, True, None):
                                each.bullet.being = False
                        else:
                            if pygame.sprite.spritecollide(each.bullet, map_stage.ironGroup, False, None):
                                each.bullet.being = False

                        # 子弹碰大本营
                        if pygame.sprite.collide_rect(each.bullet, myhome):
                            each.bullet.being = False
                            myhome.set_dead()
                            return Result("lose", None)
            else:
                enemytanksGroup.remove(each)
                tanksGroup.remove(each)

        # 家
        screen.blit(myhome.home, myhome.rect)

        # 食物
        for myfood in myfoodsGroup:
            # 食物消失
            if (not myfood.being) or (myfood.time <= 0):
                myfood.being = False
                myfoodsGroup.remove(myfood)
                continue

            # 食物还在，绘制，存在时间递减
            screen.blit(myfood.food, myfood.rect)
            myfood.time -= 1

            # 监测是否有坦克能够吃到食物
            for tank_player in mytanksGroup:
                # 未接触到食物，跳过
                if not pygame.sprite.collide_rect(tank_player, myfood):
                    continue

                # 消灭当前所有敌人
                if myfood.kind == 0:
                    for _ in enemytanksGroup:
                        resources.bang_sound.play()
                    enemytanksGroup = pygame.sprite.Group()
                    enemytanks_total -= enemytanks_now
                    enemytanks_now = 0

                # 敌人静止
                if myfood.kind == 1:
                    for each in enemytanksGroup:
                        each.can_move = False

                # 子弹增强
                if myfood.kind == 2:
                    resources.add_sound.play()
                    tank_player.bullet.stronger = True

                # 使得大本营的墙变为钢板
                if myfood.kind == 3:
                    map_stage.protect_home()

                # 坦克获得一段时间的保护罩
                if myfood.kind == 4:
                    resources.add_sound.play()
                    for tank_player in mytanksGroup:
                        tank_player.protected = True

                # 坦克升级
                if myfood.kind == 5:
                    resources.add_sound.play()
                    tank_player.up_level()

                # 坦克生命+1
                if myfood.kind == 6:
                    resources.add_sound.play()
                    tank_player.life += 1

                # 食物被吃
                myfood.being = False
                myfoodsGroup.remove(myfood)
                break

        # 将游戏的屏幕缓冲区内容更新到显示器上，也就是刷新屏幕
        pygame.display.flip()
        # 控制游戏循环的最大帧率（60）
        clock.tick(60)