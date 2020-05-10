# -*- coding:utf-8 -*-
import pygame
import sys
import os
from pygame.locals import *
from pygame.font import *
import time
import random
import win32api, win32con


# 按钮类
class Button(object):
    # 构造函数
    def __init__(self, buttonUpImage, buttonDownImage, pos):
        # 按钮未按下的图片样式
        self.buttonUp = pygame.image.load(buttonUpImage).convert_alpha()
        # 按钮按下的图片样式
        self.buttonDown = pygame.image.load(buttonDownImage).convert_alpha()
        # 按钮在窗口中的位置
        self.pos = pos

    # 检查鼠标是否在按钮图片范围内
    def inButtonRange(self):
        # 获取鼠标的位置
        mouseX, mouseY = pygame.mouse.get_pos()
        x, y = self.pos
        w, h = self.buttonUp.get_size()
        inX = x - w / 2 < mouseX < x + w / 2
        inY = y - h / 2 < mouseY < y + h / 2
        return inX and inY

    # 在窗口中显示按钮
    def show(self, screen):
        w, h = self.buttonUp.get_size()
        x, y = self.pos
        # 根据鼠标位置变换样式
        if self.inButtonRange():
            screen.blit(self.buttonDown, (x - w / 2, y - h / 2))
        else:
            screen.blit(self.buttonUp, (x - w / 2, y - h / 2))


class Hero(object):
    # 玩家 英雄类
    def __init__(self, screen_temp):
        self.x = 210
        self.y = 700
        self.life = 21
        # self.life = 100
        self.image = pygame.image.load("./Feijidazhan/img/hero1.png")
        self.screen = screen_temp
        self.bullet_list = []  # 用来存储子弹对象的引用
        # 爆炸效果用的如下属性
        self.hit = False  # 表示是否要爆炸
        self.bomb_list = []  # 用来存储爆炸时需要的图片
        self.__create_images()  # 调用这个方法向bomb_list中添加图片
        self.image_num = 0  # 用来记录while True的次数,当次数达到一定值时才显示一张爆炸的图,然后清空,,当这个次数再次达到时,再显示下一个爆炸效果的图片
        self.image_index = 0  # 用来记录当前要显示的爆炸效果的图片的序号

    def __create_images(self):
        # 添加爆炸图片
        self.bomb_list.append(pygame.image.load("./Feijidazhan/img/hero_blowup_n1.png"))
        self.bomb_list.append(pygame.image.load("./Feijidazhan/img/hero_blowup_n2.png"))
        self.bomb_list.append(pygame.image.load("./Feijidazhan/img/hero_blowup_n3.png"))
        self.bomb_list.append(pygame.image.load("./Feijidazhan/img/hero_blowup_n4.png"))

    def display(self):
        # 显示玩家的飞机
        # 如果被击中,就显示爆炸效果,否则显示普通的飞机效果
        if self.hit:
            self.screen.blit(self.bomb_list[self.image_index], (self.x, self.y))  # (self.x, self.y)是指当前英雄的位置
            # blit方法 （一个对象，左上角位置）
            self.image_num += 1
            print(self.image_num)
            if self.image_num == 7:
                self.image_num = 0
                self.image_index += 1
                print(self.image_index)  # 这里子弹打住英雄时没有被清除掉，所以打一下，就死了
            if self.image_index > 3:
                self.image_index = 0
                time.sleep(1)
                return 0
        else:
            if self.x < 0:  # 控制英雄，不让它跑出界面
                self.x = 0
            elif self.x > 382:
                self.x = 382
            if self.y < 0:
                self.y = 0
            elif self.y > 750:
                self.y = 750
            self.screen.blit(self.image, (self.x, self.y))  # z这里是只要没有被打中，就一直是刚开始的样子

        # 不管玩家飞机是否被击中,都要显示发射出去的子弹
        for bullet in self.bullet_list:
            bullet.display()
            bullet.move()

        return 1

    def move(self, move_x, move_y):
        self.x += move_x
        self.y += move_y

    def fire(self):
        # 通过创建一个子弹对象,完成发射子弹
        bullet = Bullet(self.screen, self.x, self.y)  # 创建一个子弹对象
        self.bullet_list.append(bullet)

    def bomb(self):
        self.hit = True

    def judge(self):
        global life
        if life <= 0:
            self.bomb()


class Bullet(object):
    # 玩家子弹类
    def __init__(self, screen_temp, x_temp, y_temp):
        self.x = x_temp + 40
        self.y = y_temp - 20
        self.image = pygame.image.load("./Feijidazhan/img/bullet.png")
        self.screen = screen_temp

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.y -= 10


class Bullet_Enemy(object):
    # 敌机子弹类
    def __init__(self, screen_temp, x_temp, y_temp):
        self.x = x_temp + 25
        self.y = y_temp + 30
        self.image = pygame.image.load("./Feijidazhan/img/bullet1.png")
        self.screen = screen_temp

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    def move(self, hero):
        self.y += 10
        global life
        if (hero.y <= self.y and self.y <= hero.y + 40) and (hero.x <= self.x and self.x <= hero.x + 100):
            # if self.y in range(hero.y, hero.y + 40) and self.x in range(hero.x, hero.x + 40):
            life -= 10
            # self.bullet_list.remove()
            print("---judge_enemy---")
            if life <= 0:
                hero.bomb()
            return True
        return False


class Bullet_Boss(object):
    # boss子弹类1
    def __init__(self, screen_temp, x_temp, y_temp):
        self.x = x_temp + 80
        self.y = y_temp + 230
        self.image = pygame.image.load("./Feijidazhan/img/bullet2.png")
        self.screen = screen_temp

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    def move(self, hero):
        self.y += 6
        self.x += 2
        global life
        if (hero.y <= self.y and self.y <= hero.y + 40) and (hero.x <= self.x and self.x <= hero.x + 100):
            # if self.y in range(hero.y, hero.y + 40) and self.x in range(hero.x, hero.x + 40):
            life -= 20
            # self.bullet_list.remove()
            print("---judge_boss---")
            if life <= 0:
                hero.bomb()
            return True
        return False


class Bullet_Boss1(object):
    # boss子弹类2
    def __init__(self, screen_temp, x_temp, y_temp):
        self.x = x_temp + 80
        self.y = y_temp + 230
        self.image = pygame.image.load("./Feijidazhan/img/bullet2.png")
        self.screen = screen_temp

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    def move(self, hero):
        self.y += 6
        self.x -= 2
        global life
        if (hero.y <= self.y and self.y <= hero.y + 40) and (hero.x <= self.x and self.x <= hero.x + 100):
            # if self.y in range(hero.y, hero.y + 40) and self.x in range(hero.x, hero.x + 40):
            life -= 20
            # self.bullet_list.remove()
            print("---judge_boss---")
            if life <= 0:
                hero.bomb()
            return True
        return False


class Bullet_Boss2(object):
    # boss子弹类3
    def __init__(self, screen_temp, x_temp, y_temp):
        self.x = x_temp + 80
        self.y = y_temp + 230
        self.image = pygame.image.load("./Feijidazhan/img/bullet2.png")
        self.screen = screen_temp

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    def move(self, hero):
        self.y += 6
        global life
        if (hero.y <= self.y and self.y <= hero.y + 40) and (hero.x <= self.x and self.x <= hero.x + 100):
            # if self.y in range(hero.y, hero.y + 40) and self.x in range(hero.x, hero.x + 40):
            life -= 20
            # self.bullet_list.remove()
            print("---judge_boss---")
            if life <= 0:
                hero.bomb()
            return True
        return False


class Base(object):
    # 基类 类似于抽象类
    def __init__(self, screen_temp, x, y, image_name):
        self.x = x
        self.y = y
        self.screen = screen_temp
        self.image = pygame.image.load(image_name)
        self.alive = True

    def display(self):
        if self.alive == True:
            self.screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.y += 5


class bomb_bullet(Base):
    # 炸弹类
    def __init__(self, screen_temp):
        Base.__init__(self, screen_temp, random.randint(45, 400), 0, "./Feijidazhan/img/bomb.png")

    def judge(self, hero):
        if (hero.y <= self.y and self.y <= hero.y + 40) and (hero.x <= self.x and self.x <= hero.x + 100):
            self.alive = False
            hero.bomb()

        if self.y >= 850:
            # self.alive = False
            self.y = 0
            self.x = random.randint(45, 400)
            # print("bomb.y = %d"%self.y)


class supply(Base):
    # 补给类
    def __init__(self, screen_temp):
        Base.__init__(self, screen_temp, random.randint(45, 400), -300, "./Feijidazhan/img/bomb-1.gif")

    def judge(self, hero):
        global life
        if (hero.y <= self.y and self.y <= hero.y + 40) and (hero.x <= self.x and self.x <= hero.x + 100):
            self.alive = False
            life += 10

        if self.y >= 1500:
            self.y = 0
            self.x = random.randint(45, 400)
            self.alive = True


class clear_bullet(Base):
    def __init__(self, screen_temp):
        Base.__init__(self, screen_temp, random.randint(45, 400), 0, "./Feijidazhan/img/bomb-2.gif")
        self.alive = False

    def judge(self, hero, enemies):
        global q
        q += 1
        # self.move()
        if q == 20:
            # self.move()
            self.alive = True
            q = 0
            if (hero.y <= self.y and self.y <= hero.y + 40) and (hero.x <= self.x and self.x <= hero.x + 100):
                self.alive = False
                for enemy in enemies:
                    enemy.hit == True


class EnemyPlane(object):
    # 敌机类
    def __init__(self, screen_temp):
        self.x = random.randint(15, 480)
        self.y = 0
        self.image = pygame.image.load("./Feijidazhan/img/enemy0.png")
        self.screen = screen_temp
        self.bullet_list = []  # 用来存储子弹对象的引用
        # self.direction = "right"#用来设置这个飞机默认的移动方向
        self.hit = False
        self.bomb_list = []
        self.__create_images()
        self.image_num = 0
        self.image_index = 0
        # 利用产生的随机数，随机确定飞机初始移动方向
        self.k = random.randint(1, 20)
        if self.k <= 10:
            self.direction = "right"
        elif self.k > 10:
            self.direction = "left"

    def display(self, hero):
        # 显示敌人的飞机
        if not self.hit:
            self.screen.blit(self.image, (self.x, self.y))
        else:
            self.screen.blit(self.bomb_list[self.image_index], (self.x, self.y))
            self.image_num += 1
            if self.image_num == 3 and self.image_index < 3:
                self.image_num = 0
                self.image_index += 1
                # print(self.image_index)
            # if self.image_index > 2:
            #  time.sleep(0.1)

        for bullet in self.bullet_list:
            bullet.display()
            if (bullet.move(hero)):
                self.bullet_list.remove(bullet)

    def move(self):
        # 利用随机数来控制飞机移动距离，以及移动范围
        d1 = random.uniform(1, 3)
        d2 = random.uniform(0.2, 3)
        p1 = random.uniform(50, 100)
        p2 = random.uniform(-200, 0)
        if self.direction == "right":
            self.x += d1
        elif self.direction == "left":
            self.x -= d1

        if self.x > 480 - p1:
            # 480 - 50
            self.direction = "left"
        elif self.x < p2:
            self.direction = "right"
        self.y += d2

    def bomb(self):
        self.hit = True

    def __create_images(self):
        self.bomb_list.append(pygame.image.load("./Feijidazhan/img/enemy0_down1.png"))
        self.bomb_list.append(pygame.image.load("./Feijidazhan/img/enemy0_down2.png"))
        self.bomb_list.append(pygame.image.load("./Feijidazhan/img/enemy0_down3.png"))
        self.bomb_list.append(pygame.image.load("./Feijidazhan/img/enemy0_down4.png"))

    def fire(self):
        # 利用随机数来控制敌机的开火，1/80的概率
        s = random.randint(0, 800)
        bullet1 = Bullet_Enemy(self.screen, self.x, self.y)
        if s < 10:
            self.bullet_list.append(bullet1)


class EnemyPlanes(EnemyPlane):
    # 敌机群类 继承自EnemyPlane类
    def __init__(self, screen_temp):
        EnemyPlane.__init__(self, screen_temp)
        self.num = 0
        self.enemy_list = []  # 用列表存储产生的多架敌机
        self.screen = screen_temp

    def add_enemy(self, num):
        # 产生多架敌机的函数
        self.num = num
        for i in range(num):
            enemy = EnemyPlane(self.screen)
            self.enemy_list.append(enemy)

    def display(self, hero):
        for i in range(self.num):
            self.enemy_list[i].display(hero)

    def move(self):
        for i in range(self.num):
            self.enemy_list[i].move()

    def fire(self):
        # s = random.randint(0,1000)
        for i in range(self.num):
            self.enemy_list[i].fire()


class Boss(EnemyPlane):
    # boss敌机类 继承自EnemyPlane类
    def __init__(self, screen_temp):
        EnemyPlane.__init__(self, screen_temp)
        self.x = 150
        self.y = 0
        self.bomb_list = []
        self.__create_images()
        self.image = pygame.image.load("./Feijidazhan/img/enemy2.png")
        self.screen = screen_temp
        self.bullet_list = []

    def __create_images(self):
        # self.bomb_list.append(pygame.image.load("./Feijidazhan/img/enemy2.png"))
        self.bomb_list.append(pygame.image.load("./Feijidazhan/img/enemy2.png"))
        self.bomb_list.append(pygame.image.load("./Feijidazhan/img/enemy2_down1.png"))
        self.bomb_list.append(pygame.image.load("./Feijidazhan/img/enemy2_down2.png"))
        self.bomb_list.append(pygame.image.load("./Feijidazhan/img/enemy2_down3.png"))
        self.bomb_list.append(pygame.image.load("./Feijidazhan/img/enemy2_down4.png"))
        self.bomb_list.append(pygame.image.load("./Feijidazhan/img/enemy2_down5.png"))
        self.bomb_list.append(pygame.image.load("./Feijidazhan/img/enemy2_down6.png"))

    def display(self, hero):
        # 显示敌人的飞机
        global g
        # print(g)
        self.screen.blit(self.bomb_list[g], (self.x, self.y))
        for bullet in self.bullet_list:
            bullet.display()
            if (bullet.move(hero)):
                self.bullet_list.remove(bullet)

    def move(self):
        d1 = 0
        self.y += 0

    def fire(self):
        global s
        s += 1
        bullet1 = Bullet_Boss(self.screen, self.x, self.y)
        bullet2 = Bullet_Boss1(self.screen, self.x, self.y)
        bullet3 = Bullet_Boss2(self.screen, self.x, self.y)
        if s == 20:
            s = 0
            self.bullet_list.append(bullet1)
            self.bullet_list.append(bullet2)
            self.bullet_list.append(bullet3)


def judge1(hero, enemy):
    # 判断敌机的炸毁
    for bullet1 in hero.bullet_list:
        if bullet1.y in range(int(enemy.y), int(enemy.y + 30)) and bullet1.x in range(int(enemy.x - 10),
                                                                                      int(enemy.x + 50)):
            hero.bullet_list.remove(bullet1)
            enemy.bomb()
        if bullet1.y < 0 or bullet1.x < 0 or bullet1.x > 480:  # 删除越界的玩家子弹
            hero.bullet_list.remove(bullet1)


def judge3(hero, boss):
    # 判断boss的炸毁
    global goal, g, goal0
    for bullet3 in hero.bullet_list:
        if bullet3.y in range(int(boss.y), int(boss.y + 60)) and bullet3.x in range(int(boss.x), int(boss.x + 100)):
            hero.bullet_list.remove(bullet3)
            g += 1
            boss.image = boss.bomb_list[g]
            print("g = %d" % g)
            if g >= 6:
                boss.y, g, goal = 0, 0, 0
                boss.bomb()
                goal0 += 10


def clear_enemy(enemies):
    # 清除敌机群类中被炸毁的敌机
    global goal, goal0
    for enemy in enemies.enemy_list:
        if enemy.hit == True and enemy.image_index == 3:
            enemies.enemy_list.remove(enemy)
            enemies.num -= 1
            goal += 1
            goal0 += 5
            print("goal = %d" % goal)
        if enemy.y >= 850:
            enemies.enemy_list.remove(enemy)
            enemies.num -= 1


def judge_num(enemies):
    # 判断频幕上敌人的数量，如果为零，继续添加敌人
    n = random.randint(1, 5)
    if len(enemies.enemy_list) == 0:
        enemies.add_enemy(n)


def show_text(screen_temp):
    # 在屏幕上显示文字
    text = "得分:" + str(goal0) + "  生命值:" + str(life)
    font_size = 30
    pos = (0, 0)
    color = (0, 0, 0)
    cur_font = pygame.font.SysFont("simsunnsimsun", font_size)
    text_fmt = cur_font.render(text, 1, color)
    screen_temp.blit(text_fmt, pos)


def creat_bomb(screen_temp):
    bomb = bomb_bullet(screen_temp)
    bomb_list = []
    bomb_list.apend(bomb)


# 显示关卡选择界面的函数
def showChapterInterface(screen, chapter1):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            # 如果点击的是“第一关”
            if chapter1.inButtonRange():
                return 1
    # 显示“第一关”按钮
    chapter1.show(screen)
    return 0


def recordScore(score):
    filename = './Feijidazhan/score.dat'
    if os.path.isfile(filename):
        fp = open(filename, 'r')
        readscore = fp.read()
        fp.close()
        if readscore:
            if score > int(readscore):
                fp = open(filename, 'w')
                fp.write(str(score))
                fp.close()
        else:
            fp = open(filename, 'w')
            fp.write(str(score))
            fp.close()
    else:
        fp = open(filename, 'w')
        fp.write(str(score))
        fp.close()


# 定义的全局变量
goal = 0  # 玩家得分
goal0 = 0
g = 0  # 击中boss的次数
life = 100  # 生命值
s = 0  # 判断大boss是否发射子弹
q = 0


def main():
    global goal, goal0, g, life, s, q
    # 主函数执行
    # 获取事件，比如按键等

    pygame.init()

    screen = pygame.display.set_mode((480, 852), 0, 32)
    background = pygame.image.load("./Feijidazhan/img/background.png")
    pygame.display.set_caption("飞机大战")

    atlas = pygame.image.load("./Feijidazhan/img/New Atlas.png")

    name = pygame.image.load("./Feijidazhan/img/name.png")
    # “开始游戏”按钮
    start_game = Button('./Feijidazhan/img/GameStartUp.png', './Feijidazhan/img/GameStartDown.png', (230, 500))

    while True:

        # 全局变量
        goal = 0  # 玩家得分
        goal0 = 0
        g = 0  # 击中boss的次数
        life = 100  # 生命值
        s = 0  # 判断大boss是否发射子弹
        q = 0

        bb = False
        move_x = 0
        move_y = 0

        # 创建玩家飞机
        hero = Hero(screen)
        # 创建敌机群
        enemis = EnemyPlanes(screen)
        enemis.add_enemy(5)
        # 创建boss对象
        boss = Boss(screen)
        # 创建炸弹对象
        bomb = bomb_bullet(screen)
        # 创建补给对象
        supply0 = supply(screen)
        clear = clear_bullet(screen)
        left_key, right_key, up_key, down_key, done = 0, 0, 0, 0, 0
        # mark = 0#用来判断boss发射子弹

        # 绘制背景图片
        screen.blit(background, (0, 0))
        screen.blit(name, (20, 150))
        chapter = showChapterInterface(screen, start_game) - 1
        if chapter == -1:
            pygame.display.update()
            continue

        while True:
            start_flag = True
            if done:
                if done % 8 == 0:
                    done = 1
                    hero.fire()
                else:
                    done += 1
            for event in pygame.event.get():
                # 判断是否是点击了退出按钮
                if event.type == QUIT:
                    print("exit")
                    exit()
                # 判断是否是按下了键
                if event.type == KEYDOWN:
                    # down
                    # 检测按键是否是a或者left

                    if event.key == K_a or event.key == K_LEFT:
                        # print('left')
                        move_x = -5
                        left_key += 1

                    # 检测按键是否是d或者right
                    elif event.key == K_d or event.key == K_RIGHT:
                        # print('right')
                        move_x = 5
                        right_key += 1

                    elif event.key == K_w or event.key == K_UP:
                        move_y = -5
                        up_key += 1

                    elif event.key == K_s or event.key == K_DOWN:
                        move_y = 5
                        down_key += 1

                    # 检测按键是否是空格键
                    elif event.key == K_SPACE:
                        # print('space')
                        hero.fire()
                        done = 1
                        # enemis.fire()

                    elif event.key == K_b:
                        print('b')
                        hero.bomb()

                if event.type == KEYUP:
                    if event.key == K_a or event.key == K_LEFT:
                        left_key -= 1
                        if right_key == 0:
                            move_x = 0
                        else:
                            move_x = 5

                    if event.key == K_d or event.key == K_RIGHT:
                        right_key -= 1
                        if left_key == 0:
                            move_x = 0
                        else:
                            move_x = -5

                    if event.key == K_w or event.key == K_UP:
                        up_key -= 1
                        if down_key == 0:
                            move_y = 0
                        else:
                            move_y = 5

                    if event.key == K_s or event.key == K_DOWN:
                        down_key -= 1
                        if up_key == 0:
                            move_y = 0
                        else:
                            move_y = -5

                    if event.key == K_SPACE:
                        done = 0

            screen.blit(background, (0, 0))
            hero.move(move_x, move_y)
            if not hero.display():
                start_flag = False
                win32api.MessageBox(0, "游戏结束！\n你的得分为：%d" % goal0, "游戏结束", win32con.MB_OK)
                recordScore(goal0)
                break
            hero.judge()
            enemis.display(hero)
            enemis.move()
            enemis.fire()
            bomb.display()
            bomb.judge(hero)
            bomb.move()
            supply0.display()
            supply0.judge(hero)
            supply0.move()
            # clear.display()
            # clear.judge(hero, enemis)
            # clear.move()
            for i in range(enemis.num):
                judge1(hero, enemis.enemy_list[i])
                # enemis.enemy_list[i].judge(hero)
            clear_enemy(enemis)
            judge_num(enemis)
            show_text(screen)
            if goal >= 15:
                boss.display(hero)
                boss.move()
                # mark+=1
                # if mark==8:
                boss.fire()
                # mark = 0
                # boss.judge
                judge3(hero, boss)
            pygame.display.update()
            if not start_flag:
                break


if __name__ == "__main__":
     main()