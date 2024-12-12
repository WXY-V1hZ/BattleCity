# import sys
#
# import pygame
#
# from entity import home, scene, tank, food
# from views import ui, menu
#
# width = 630
# height = 630
#
# # 主函数
# def main ():
#     # 初始化
#     pygame.init()
#     pygame.mixer.init()
#
#     # 设置窗口大小
#     screen = pygame.display.set_mode((width, height))
#     # 设置窗口标题
#     pygame.display.set_caption("坦克大战")
#
#     # 加载图片
#     bg_img = pygame.image.load("assets/images/others/background.png")
#     # 加载音效
#     add_sound = pygame.mixer.Sound("assets/audios/add.wav")
#     add_sound.set_volume(1)
#     bang_sound = pygame.mixer.Sound("assets/audios/bang.wav")
#     bang_sound.set_volume(1)
#     blast_sound = pygame.mixer.Sound("assets/audios/blast.wav")
#     blast_sound.set_volume(1)
#     fire_sound = pygame.mixer.Sound("assets/audios/fire.wav")
#     fire_sound.set_volume(1)
#     Gunfire_sound = pygame.mixer.Sound("assets/audios/Gunfire.wav")
#     Gunfire_sound.set_volume(1)
#     hit_sound = pygame.mixer.Sound("assets/audios/hit.wav")
#     hit_sound.set_volume(1)
#     start_sound = pygame.mixer.Sound("assets/audios/start.wav")
#     start_sound.set_volume(1)
#
#     # 开始界面，获取玩家数量
#     num_player = ui.show_start(screen, width, height)
#     # 播放游戏开始的音乐
#     start_sound.play()
#
#     # 关卡
#     stage = 0
#     num_stage = 2
#     # 游戏是否结束
#     is_gameover = False
#     # 时钟
#     clock = pygame.time.Clock()
#
#     # 主循环
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#
#         # 关卡递增
#         stage += 1
#         # 通关或者失败，退出
#         if stage > num_stage or is_gameover:
#             break
#
#         # 显示关卡界面
#         ui.show_switch_stage(screen, width, width, stage)
#
#         # 该关卡坦克总数量
#         enemytanks_total = min(stage * 12, 60)
#         # 场上存在的敌方坦克总数量
#         enemytanks_now = 0
#         # 场上可以存在的敌方坦克总数量
#         enemytanks_now_max = min(max(stage * 2, 4), 8)
#
#         # 精灵组
#         tanksGroup = pygame.sprite.Group()
#         mytanksGroup = pygame.sprite.Group()
#         enemytanksGroup = pygame.sprite.Group()
#         enemybulletsGroup = pygame.sprite.Group()
#         myfoodsGroup = pygame.sprite.Group()
#
#         # 自定义事件
#         # 	-生成敌方坦克事件
#         genEnemyEvent = pygame.constants.USEREVENT + 0
#         pygame.time.set_timer(genEnemyEvent, 100)
#         # 	-敌方坦克静止恢复事件
#         recoverEnemyEvent = pygame.constants.USEREVENT + 1
#         pygame.time.set_timer(recoverEnemyEvent, 8000)
#         # 	-我方坦克无敌恢复事件
#         noprotectMytankEvent = pygame.constants.USEREVENT + 2
#         pygame.time.set_timer(noprotectMytankEvent, 8000)
#
#         # 资源初始化
#         # 关卡地图
#         # TODO: 地图编辑器
#         map_stage = scene.Map(stage)
#         # 我方坦克 TODO: 重构坦克类
#         tank_player1 = tank.myTank(1)
#         tanksGroup.add(tank_player1)
#         mytanksGroup.add(tank_player1)
#         if num_player > 1:
#             tank_player2 = tank.myTank(2)
#             tanksGroup.add(tank_player2)
#             mytanksGroup.add(tank_player2)
#
#         # 状态初始化
#         is_switch_tank = True
#         player1_moving = False
#         player2_moving = False
#         # 为了轮胎的动画效果
#         time = 0
#
#         # 敌方坦克，最多三辆
#         for i in range(0, 3):
#             if enemytanks_total > 0:
#                 enemytank = tank.enemyTank(i)
#                 tanksGroup.add(enemytank)
#                 enemytanksGroup.add(enemytank)
#                 enemytanks_now += 1
#                 enemytanks_total -= 1
#
#         # 大本营
#         myhome = home.Home()
#
#         # 加载出场特效，根据图像大小提取帧
#         appearance_img = pygame.image.load("assets/images/others/appear.png").convert_alpha()
#         appearances = []
#         appearances.append(appearance_img.subsurface((0, 0), (48, 48)))
#         appearances.append(appearance_img.subsurface((48, 0), (48, 48)))
#         appearances.append(appearance_img.subsurface((96, 0), (48, 48)))
#
#         # 关卡主循环
#         while True:
#
#             # 失败
#             if is_gameover is True:
#                 break
#             # 胜利
#             if enemytanks_total < 1 and enemytanks_now < 1:
#                 is_gameover = False
#                 break
#
#             # 事件监测
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     sys.exit()
#                 elif event.type == pygame.KEYDOWN:
#                     if not menu.listen(screen, width, height, event):
#                         break
#
#                 # 增加坦克事件，检验是否还有敌方坦克 且 场上是否还能增加坦克
#                 if event.type == genEnemyEvent and enemytanks_total > 0 and enemytanks_now < enemytanks_now_max:
#                     enemytank = tank.enemyTank()
#                     # 检验生成位置是否与其他坦克重叠
#                     if pygame.sprite.spritecollide(enemytank, tanksGroup, False, None):
#                         continue
#                     tanksGroup.add(enemytank)
#                     enemytanksGroup.add(enemytank)
#                     enemytanks_now += 1
#                     enemytanks_total -= 1
#
#                 # 恢复坦克的禁锢状态
#                 if event.type == recoverEnemyEvent:
#                     for each in enemytanksGroup:
#                         each.can_move = True
#
#                 # 移除我方坦克的无敌状态
#                 if event.type == noprotectMytankEvent:
#                     for each in mytanksGroup:
#                         mytanksGroup.protected = False
#
#             # 检查用户键盘操作
#             key_pressed = pygame.key.get_pressed()
#
#             # 玩家一
#             if key_pressed[pygame.K_w]:
#                 tanksGroup.remove(tank_player1)
#                 tank_player1.move_up(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
#                 tanksGroup.add(tank_player1)
#                 player1_moving = True
#             elif key_pressed[pygame.K_s]:
#                 tanksGroup.remove(tank_player1)
#                 tank_player1.move_down(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
#                 tanksGroup.add(tank_player1)
#                 player1_moving = True
#             elif key_pressed[pygame.K_a]:
#                 tanksGroup.remove(tank_player1)
#                 tank_player1.move_left(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
#                 tanksGroup.add(tank_player1)
#                 player1_moving = True
#             elif key_pressed[pygame.K_d]:
#                 tanksGroup.remove(tank_player1)
#                 tank_player1.move_right(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
#                 tanksGroup.add(tank_player1)
#                 player1_moving = True
#             elif key_pressed[pygame.K_j]:
#                 if not tank_player1.bullet.being:
#                     fire_sound.play()
#                     tank_player1.shoot()
#
#             # 玩家二
#             if num_player > 1:
#                 if key_pressed[pygame.K_UP]:
#                     tanksGroup.remove(tank_player2)
#                     tank_player2.move_up(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
#                     tanksGroup.add(tank_player2)
#                     player2_moving = True
#                 elif key_pressed[pygame.K_DOWN]:
#                     tanksGroup.remove(tank_player2)
#                     tank_player2.move_down(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
#                     tanksGroup.add(tank_player2)
#                     player2_moving = True
#                 elif key_pressed[pygame.K_LEFT]:
#                     tanksGroup.remove(tank_player2)
#                     tank_player2.move_left(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
#                     tanksGroup.add(tank_player2)
#                     player2_moving = True
#                 elif key_pressed[pygame.K_RIGHT]:
#                     tanksGroup.remove(tank_player2)
#                     tank_player2.move_right(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
#                     tanksGroup.add(tank_player2)
#                     player2_moving = True
#                 elif key_pressed[pygame.K_0]:
#                     if not tank_player2.bullet.being:
#                         fire_sound.play()
#                         tank_player2.shoot()
#
#             # 绘制背景
#             screen.blit(bg_img, (0, 0))
#             # 石头墙
#             for each in map_stage.brickGroup:
#                 screen.blit(each.brick, each.rect)
#             # 钢墙
#             for each in map_stage.ironGroup:
#                 screen.blit(each.iron, each.rect)
#             # 冰
#             for each in map_stage.iceGroup:
#                 screen.blit(each.ice, each.rect)
#             # 河流
#             for each in map_stage.riverGroup:
#                 screen.blit(each.river, each.rect)
#             # 树
#             for each in map_stage.treeGroup:
#                 screen.blit(each.tree, each.rect)
#
#             time += 1
#             if time == 5:
#                 time = 0
#                 is_switch_tank = not is_switch_tank
#
#             # 我方坦克，玩家1
#             if tank_player1 in mytanksGroup:
#                 if is_switch_tank and player1_moving:
#                     screen.blit(tank_player1.tank_0, (tank_player1.rect.left, tank_player1.rect.top))
#                     player1_moving = False
#                 else:
#                     screen.blit(tank_player1.tank_1, (tank_player1.rect.left, tank_player1.rect.top))
#                 if tank_player1.protected:
#                     screen.blit(tank_player1.protected_mask1, (tank_player1.rect.left, tank_player1.rect.top))
#             # 玩家2
#             if num_player > 1:
#                 if tank_player2 in mytanksGroup:
#                     if is_switch_tank and player2_moving:
#                         screen.blit(tank_player2.tank_0, (tank_player2.rect.left, tank_player2.rect.top))
#                         player1_moving = False
#                     else:
#                         screen.blit(tank_player2.tank_1, (tank_player2.rect.left, tank_player2.rect.top))
#                     if tank_player2.protected:
#                         screen.blit(tank_player1.protected_mask1, (tank_player2.rect.left, tank_player2.rect.top))
#
#             # 敌方坦克
#             for each in enemytanksGroup:
#                 # 出生特效
#                 if each.born:
#                     if each.times > 0:
#                         each.times -= 1
#                         if each.times <= 10:
#                             screen.blit(appearances[2], (3 + each.x * 12 * 24, 3))
#                         elif each.times <= 20:
#                             screen.blit(appearances[1], (3 + each.x * 12 * 24, 3))
#                         elif each.times <= 30:
#                             screen.blit(appearances[0], (3 + each.x * 12 * 24, 3))
#                         elif each.times <= 40:
#                             screen.blit(appearances[2], (3 + each.x * 12 * 24, 3))
#                         elif each.times <= 50:
#                             screen.blit(appearances[1], (3 + each.x * 12 * 24, 3))
#                         elif each.times <= 60:
#                             screen.blit(appearances[0], (3 + each.x * 12 * 24, 3))
#                         elif each.times <= 70:
#                             screen.blit(appearances[2], (3 + each.x * 12 * 24, 3))
#                         elif each.times <= 80:
#                             screen.blit(appearances[1], (3 + each.x * 12 * 24, 3))
#                         elif each.times <= 90:
#                             screen.blit(appearances[0], (3 + each.x * 12 * 24, 3))
#                     else:
#                         each.born = False
#                 else:
#                     if is_switch_tank:
#                         screen.blit(each.tank_0, (each.rect.left, each.rect.top))
#                     else:
#                         screen.blit(each.tank_1, (each.rect.left, each.rect.top))
#                     if each.can_move:
#                         tanksGroup.remove(each)
#                         each.move(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
#                         tanksGroup.add(each)
#
#             # 我方子弹 TODO：重构子弹类
#             for tank_player in mytanksGroup:
#                 # 子弹不存在，跳过
#                 if not tank_player.bullet.being:
#                     continue
#
#                 # 子弹运动
#                 tank_player.bullet.move()
#                 screen.blit(tank_player.bullet.bullet, tank_player.bullet.rect)
#
#                 # 子弹碰撞敌方子弹
#                 for each in enemybulletsGroup:
#                     # 敌方子弹不存在，跳过
#                     if not each.being:
#                         enemybulletsGroup.remove(each)
#                         continue
#
#                     # 没有碰撞
#                     if not pygame.sprite.collide_rect(tank_player.bullet, each):
#                         continue
#
#                     # 碰撞
#                     tank_player.bullet.being = False
#                     each.being = False
#                     enemybulletsGroup.remove(each)
#                     break
#
#                 # 子弹碰撞敌方坦克
#                 for each in enemytanksGroup:
#                     # 敌方坦克不存在，跳过
#                     if not each.being:
#                         enemytanksGroup.remove(each)
#                         tanksGroup.remove(each)
#                         continue
#
#                     # 没有碰撞
#                     if not pygame.sprite.collide_rect(tank_player.bullet, each):
#                         continue
#
#                     # 碰撞
#                     if each.is_red == True:
#                         myfood = food.Food()
#                         myfood.generate()
#                         myfoodsGroup.add(myfood)
#                         each.is_red = False
#                     each.blood -= 1
#                     each.color -= 1
#                     if each.blood < 0:
#                         bang_sound.play()
#                         each.being = False
#                         enemytanksGroup.remove(each)
#                         enemytanks_now -= 1
#                         tanksGroup.remove(each)
#                     else:
#                         each.reload()
#                     tank_player.bullet.being = False
#                     break
#
#                 # 子弹碰撞石头墙
#                 if pygame.sprite.spritecollide(tank_player.bullet, map_stage.brickGroup, True, None):
#                     tank_player.bullet.being = False
#
#                 # 子弹碰钢墙
#                 if tank_player.bullet.stronger:
#                     if pygame.sprite.spritecollide(tank_player.bullet, map_stage.ironGroup, True, None):
#                         tank_player.bullet.being = False
#                 else:
#                     if pygame.sprite.spritecollide(tank_player.bullet, map_stage.ironGroup, False, None):
#                         tank_player.bullet.being = False
#
#                 # 子弹碰大本营
#                 if pygame.sprite.collide_rect(tank_player.bullet, myhome):
#                     tank_player.bullet.being = False
#                     myhome.set_dead()
#                     is_gameover = True
#
#             # 敌方子弹
#             for each in enemytanksGroup:
#                 if each.being:
#                     if each.can_move and not each.bullet.being:
#                         enemybulletsGroup.remove(each.bullet)
#                         each.shoot()
#                         enemybulletsGroup.add(each.bullet)
#                     if not each.born:
#                         if each.bullet.being:
#                             each.bullet.move()
#                             screen.blit(each.bullet.bullet, each.bullet.rect)
#                             # 子弹碰撞我方坦克
#                             for tank_player in mytanksGroup:
#                                 if pygame.sprite.collide_rect(each.bullet, tank_player):
#                                     if not tank_player.protected:
#                                         bang_sound.play()
#                                         tank_player.life -= 1
#                                         if tank_player.life < 0:
#                                             mytanksGroup.remove(tank_player)
#                                             tanksGroup.remove(tank_player)
#                                             if len(mytanksGroup) < 1:
#                                                 is_gameover = True
#                                         else:
#                                             tank_player.reset()
#                                     each.bullet.being = False
#                                     enemybulletsGroup.remove(each.bullet)
#                                     break
#                             # 子弹碰撞石头墙
#                             if pygame.sprite.spritecollide(each.bullet, map_stage.brickGroup, True, None):
#                                 each.bullet.being = False
#                                 enemybulletsGroup.remove(each.bullet)
#
#                             # 子弹碰钢墙
#                             if each.bullet.stronger:
#                                 if pygame.sprite.spritecollide(each.bullet, map_stage.ironGroup, True, None):
#                                     each.bullet.being = False
#                             else:
#                                 if pygame.sprite.spritecollide(each.bullet, map_stage.ironGroup, False, None):
#                                     each.bullet.being = False
#
#                             # 子弹碰大本营
#                             if pygame.sprite.collide_rect(each.bullet, myhome):
#                                 each.bullet.being = False
#                                 myhome.set_dead()
#                                 is_gameover = True
#                 else:
#                     enemytanksGroup.remove(each)
#                     tanksGroup.remove(each)
#
#             # 家
#             screen.blit(myhome.home, myhome.rect)
#
#             # 食物
#             for myfood in myfoodsGroup:
#                 # 食物消失
#                 if (not myfood.being) or (myfood.time <= 0):
#                     myfood.being = False
#                     myfoodsGroup.remove(myfood)
#                     continue
#
#                 # 食物还在，绘制，存在时间递减
#                 screen.blit(myfood.food, myfood.rect)
#                 myfood.time -= 1
#
#                 # 监测是否有坦克能够吃到食物
#                 for tank_player in mytanksGroup:
#                     # 未接触到食物，跳过
#                     if not pygame.sprite.collide_rect(tank_player, myfood):
#                         continue
#
#                     # 消灭当前所有敌人
#                     if myfood.kind == 0:
#                         for _ in enemytanksGroup:
#                             bang_sound.play()
#                         enemytanksGroup = pygame.sprite.Group()
#                         enemytanks_total -= enemytanks_now
#                         enemytanks_now = 0
#
#                     # 敌人静止
#                     if myfood.kind == 1:
#                         for each in enemytanksGroup:
#                             each.can_move = False
#
#                     # 子弹增强
#                     if myfood.kind == 2:
#                         add_sound.play()
#                         tank_player.bullet.stronger = True
#
#                     # 使得大本营的墙变为钢板
#                     if myfood.kind == 3:
#                         map_stage.protect_home()
#
#                     # 坦克获得一段时间的保护罩
#                     if myfood.kind == 4:
#                         add_sound.play()
#                         for tank_player in mytanksGroup:
#                             tank_player.protected = True
#
#                     # 坦克升级
#                     if myfood.kind == 5:
#                         add_sound.play()
#                         tank_player.up_level()
#
#                     # 坦克生命+1
#                     if myfood.kind == 6:
#                         add_sound.play()
#                         tank_player.life += 1
#
#                     # 食物被吃
#                     myfood.being = False
#                     myfoodsGroup.remove(myfood)
#                     break
#
#             # 将游戏的屏幕缓冲区内容更新到显示器上，也就是刷新屏幕
#             pygame.display.flip()
#             # 控制游戏循环的最大帧率（60）
#             clock.tick(60)
#
#     # 根据是否失败显示胜败界面
#     ui.show_end(screen, width, height, not is_gameover)
#
# if __name__ == '__main__':
#     main()
