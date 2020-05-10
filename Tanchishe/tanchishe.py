# coding=utf-8
import pygame
import sys
import time
import random
import os
import win32api, win32con
from pygame.locals import *

redColour = pygame.Color(255, 0, 0)
greenColour = pygame.Color(0, 255, 0)
skyblueColour = pygame.Color(0, 255, 255)
blueColour = pygame.Color(0, 0, 255)
blackColour = pygame.Color(0, 0, 0)
whiteColour = pygame.Color(255, 255, 255)
greyColour = pygame.Color(150, 150, 150)
yellowColour = pygame.Color(255, 255, 0)
purpleColour = pygame.Color(255, 0, 255)
brownColour = pygame.Color(150, 75, 75)
DeepPinkColour = pygame.Color(255, 20, 147)

# 初始化并播放背景音乐
# pygame.mixer.init()  #初始化混音器
# pygame.mixer.music.load('Ken Arai - NEXT TO YOU.mp3')  #加载背景音乐
# pygame.mixer.music.set_volume(0.2)  #设置音量
# pygame.mixer.music.play()   #播放背景音乐


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


# 定义游戏结束函数。当双方长度相等且头头相撞时，为平局。游戏结束，并显示双方分数。
def gameOver(playSurface, score1, score2):
    gameOverFont = pygame.font.SysFont('simsunnsimsun', 24)
    gameOverSurf = gameOverFont.render('平局   ' + '玩家1：' + str(score1 - 3) + '   ' + '玩家2：' + str(score2 - 3), True, whiteColour)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.midtop = (320, 10)
    playSurface.blit(gameOverSurf, gameOverRect)
    pygame.display.flip()
    recordScore(max(score1-3, score2-3))
    win32api.MessageBox(0, "游戏结束！\n\n玩家1得分为：%d\n\n玩家2得分为：%d" % (score1-3, score2-3), "游戏结束", win32con.MB_OK)


# 定义游戏结束函数。当1号玩家撞墙或被2号玩家吃了时，游戏结束，显示1号玩家失败，以及双方分数。
def gameOver1(playSurface, chapter, score):
    gameOverFont = pygame.font.SysFont('simsunnsimsun', 24)
    if chapter:
        gameOverSurf = gameOverFont.render(
            '玩家2（蓝）获胜   ' + '玩家1（红）：' + str(score[0] - 3) + '  ' + '玩家2（蓝）：' + str(score[1] - 3), True,
            whiteColour)
    else:
        gameOverSurf = gameOverFont.render(
            '你输了    ' + '得分:' + str(score[0] - 3), True, whiteColour)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.midtop = (320, 10)
    playSurface.blit(gameOverSurf, gameOverRect)
    pygame.display.flip()
    recordScore((score[0]-3) if chapter else max(score[0]-3, score[1]-3))
    if chapter:
        win32api.MessageBox(0, "游戏结束！\n\n玩家1得分为：%d\n\n玩家2得分为：%d" % (score[0]-3, score[1]-3), "游戏结束", win32con.MB_OK)
    else:
        win32api.MessageBox(0, "游戏结束！\n你的得分为：%d" % (score[0]-3), "游戏结束", win32con.MB_OK)


# 定义游戏结束函数。当2号玩家撞墙或被1号玩家吃了时，游戏结束，显示2号玩家失败，以及双方分数。
def gameOver2(playSurface,score1,score2):
    gameOverFont = pygame.font.SysFont('simsunnsimsun', 24)
    gameOverSurf = gameOverFont.render('玩家1（红）获胜   '+'玩家1（红）：'+str(score1-3)+'   '+'玩家2（蓝）：'+str(score2-3), True, whiteColour)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.midtop = (320, 10)
    playSurface.blit(gameOverSurf, gameOverRect)
    pygame.display.flip()
    recordScore(max(score1, score2))
    win32api.MessageBox(0, "游戏结束！\n\n玩家1得分为：%d\n\n玩家2得分为：%d" % (score1-3, score2-3), "游戏结束", win32con.MB_OK)


# 显示关卡选择界面的函数
def showChapterInterface(screen, interface, chapter1, chapter2):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            # 如果点击的是“第一关”
            if chapter1.inButtonRange():
                return 1
            # 如果点击的是“第二关”
            elif chapter2.inButtonRange():
                return 2
    # 绘制背景图片
    screen.blit(interface, (0, 0))
    # 显示“第一关”按钮
    chapter1.show(screen)
    # 显示“第二关”按钮
    chapter2.show(screen)
    return 0


# 记录分数
def recordScore(score):
    filename = './Tanchishe/score.dat'
    if os.path.isfile(filename):
        fp = open(filename, 'r')
        readscore = fp.read()
        if score > int(readscore):
            fp = open(filename, 'w')
            fp.write(str(score))
        fp.close()
    else:
        fp = open(filename, 'w')
        fp.write(str(score))
        fp.close()


def main():

    pygame.init()  # pygame初始化

    playSurface = pygame.display.set_mode((640, 480))  #全屏显示
    fpsClock = pygame.time.Clock()
    pygame.display.set_caption('贪吃蛇')  #欢迎界面，此时未开始游戏
    GAMESTATE = 'playing'

    # “第一关”按钮
    buttonc1 = Button('./Tanchishe/oneUp.png', './Tanchishe/oneDown.png', (300, 200))
    # “第二关”按钮
    buttonc2 = Button('./Tanchishe/twoUp.png', './Tanchishe/twoDown.png', (300, 300))
    # “第三关”按钮
    #buttonc3 = Button('Chapter3Up.png', 'Chapter3Down.png', (150, 400))

    # 选择关卡界面图片
    choosechapter = pygame.image.load("./Tanchishe/ChooseChapter.png")

    '''
    #显示欢迎界面，有开始游戏和退出游戏两个选项
    title_font = pygame.font.SysFont('arial', 32)
    welcome_words = title_font.render('Welcome to My Snake', True, (0, 0, 0), (255, 255, 255))
    tips_font = pygame.font.SysFont('arial', 24)
    start_game_words = tips_font.render('Click to Start Game', True, (0, 0, 0), (255, 255, 255))
    close_game_words = tips_font.render('Press ESC to Close', True, (0, 0, 0), (255, 255, 255))
    '''

    while True:
        chapter = showChapterInterface(playSurface, choosechapter, buttonc1, buttonc2) - 1
        if chapter == -1:
            pygame.display.update()
            continue
        # else:
        game_started = True
        #初始化两条蛇的起始位置和长度
        snakePosition1 = [100, 100]
        snakeSegments1 = [[100, 100], [80, 100], [60, 100]]
        # 初始化两条蛇的起始方向
        direction1 = 'right'
        changeDirection1 = direction1

        if chapter:
            snakePosition2 = [200, 200]
            snakeSegments2 = [[200, 200], [180, 200], [160, 200]]
            direction2 = 'right'
            changeDirection2 = direction2

        #初始化树莓的起始位置
        raspberryPosition = [300, 300]
        raspberrySpawned = 1

        while True:   #游戏循环主体
            for event in pygame.event.get():  #获取事件
                if event.type == QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:   #键盘输入
                    if event.key == K_SPACE:
                        if GAMESTATE == 'playing':
                            GAMESTATE = 'pausing'
                        elif GAMESTATE == 'pausing':
                            GAMESTATE = 'playing'
                    #方向键控制玩家1
                    if event.key == K_RIGHT:
                        changeDirection1 = 'right'
                    if event.key == K_LEFT:
                        changeDirection1 = 'left'
                    if event.key == K_UP:
                        changeDirection1 = 'up'
                    if event.key == K_DOWN:
                        changeDirection1 = 'down'

                    if chapter:
                        # ‘W’‘A’‘S’‘D’控制玩家2
                        if event.key == ord('d'):
                            changeDirection2 = 'right'
                        if event.key == ord('a'):
                            changeDirection2= 'left'
                        if event.key == ord('w'):
                            changeDirection2 = 'up'
                        if event.key == ord('s'):
                            changeDirection2 = 'down'

                    if event.key == K_ESCAPE:  #按动ESC退出游戏
                        # pygame.event.post(pygame.event.Event(QUIT))
                        game_started = False
                        break
                '''
                elif (not game_started) and event.type == pygame.MOUSEBUTTONDOWN: #在游戏欢迎界面时，根据鼠标位置判断是否开始游戏
                    x, y = pygame.mouse.get_pos()
                    if 213 <= x <= 422 and 304 <= y <= 342:
                        game_started = True
                '''
            playSurface.fill(blackColour)  #游戏画面背景为白色

            if game_started: #开始游戏

                if GAMESTATE == 'pausing':
                    continue
                # 判断是否输入了反方向,如果输入相反方向，则方向不改变
                if changeDirection1 == 'right' and direction1 != 'left':
                    direction1 = changeDirection1
                if changeDirection1 == 'left' and direction1 != 'right':
                    direction1 = changeDirection1
                if changeDirection1 == 'up' and direction1 != 'down':
                    direction1 = changeDirection1
                if changeDirection1 == 'down' and direction1 != 'up':
                    direction1 = changeDirection1

                if chapter:
                    if changeDirection2 == 'right' and direction2 != 'left':
                        direction2 = changeDirection2
                    if changeDirection2 == 'left' and direction2 != 'right':
                        direction2 = changeDirection2
                    if changeDirection2 == 'up' and direction2 != 'down':
                        direction2 = changeDirection2
                    if changeDirection2 == 'down' and direction2 != 'down':
                        direction2 = changeDirection2
                # 根据方向移动蛇头的坐标
                if direction1 == 'right':
                    snakePosition1[0] += 20
                if direction1 == 'left':
                    snakePosition1[0] -= 20
                if direction1 == 'up':
                    snakePosition1[1] -= 20
                if direction1 == 'down':
                    snakePosition1[1] += 20

                if chapter:
                    if direction2 == 'right':
                        snakePosition2[0] += 20
                    if direction2 == 'left':
                        snakePosition2[0] -= 20
                    if direction2 == 'up':
                        snakePosition2[1] -= 20
                    if direction2 == 'down':
                        snakePosition2[1] += 20

                # 增加蛇的长度
                snakeSegments1.insert(0, list(snakePosition1))
                if chapter:
                    snakeSegments2.insert(0, list(snakePosition2))
                # 判断是否吃掉了树莓
                if snakePosition1[0] == raspberryPosition[0] and snakePosition1[1] == raspberryPosition[1]:
                    raspberrySpawned = 0
                else:
                    snakeSegments1.pop()

                if chapter:
                    if snakePosition2[0] == raspberryPosition[0] and snakePosition2[1] == raspberryPosition[1]:
                        raspberrySpawned = 0
                    else:
                        snakeSegments2.pop()
                # 如果吃掉树莓，则重新生成树莓
                if raspberrySpawned == 0:
                    x = random.randrange(1, 32)
                    y = random.randrange(1, 24)
                    raspberryPosition = [int(x * 20), int(y * 20)]  #先随机在任意位置生成一个树莓

                    if chapter:
                        while raspberryPosition in snakePosition1 or raspberryPosition in snakePosition2:  #判断树莓是否声称在蛇的身体上，如果是，则重新生成树莓
                            x = random.randrange(1, 32)
                            y = random.randrange(1, 24)
                            raspberryPosition = [int(x * 20), int(y * 20)]
                        raspberrySpawned = 1
                    else:
                        while raspberryPosition in snakePosition1:  #判断树莓是否声称在蛇的身体上，如果是，则重新生成树莓
                            x = random.randrange(1, 32)
                            y = random.randrange(1, 24)
                            raspberryPosition = [int(x * 20), int(y * 20)]
                        raspberrySpawned = 1

                # 刷新pygame显示层，显示蛇以及树莓
                playSurface.fill(blackColour)

                pygame.draw.rect(playSurface, purpleColour, Rect(snakeSegments1[0][0], snakeSegments1[0][1], 20, 20))# 蛇头
                for position in snakeSegments1[1:]:
                    pygame.draw.rect(playSurface, DeepPinkColour, Rect(position[0], position[1], 20, 20))
                    colour = random.choice([whiteColour, yellowColour, redColour])
                    pygame.draw.rect(playSurface, colour, Rect(raspberryPosition[0], raspberryPosition[1], 20, 20))
                if chapter:
                    pygame.draw.rect(playSurface, skyblueColour, Rect(snakeSegments2[0][0], snakeSegments2[0][1], 20, 20))
                    for position in snakeSegments2[1:]:
                        pygame.draw.rect(playSurface, blueColour, Rect(position[0], position[1], 20, 20))
                pygame.display.flip()

                # 蛇的位置超出边框就算死亡，或者和另一条蛇相撞。
                score1 = len(snakeSegments1)   #分数
                if chapter:
                    score2 = len(snakeSegments2)
                else:
                    score2 = 0
                if snakePosition1[0] > 620 or snakePosition1[0] < 0:
                     gameOver1(playSurface, chapter, [score1, score2])
                     game_started = False
                if snakePosition1[1] > 460 or snakePosition1[1] < 0:
                     gameOver1(playSurface, chapter, [score1, score2])
                     game_started = False
                if chapter:
                    for snakeBody1 in snakeSegments1[1:]:  # 玩家二撞上了玩家一，玩家二失败
                        if snakePosition2[0] == snakeBody1[0] and snakePosition2[1] == snakeBody1[1]:
                            gameOver2(playSurface, score1, score2)
                            game_started = False
                            break
                    if snakePosition2[0] > 620 or snakePosition2[0] < 0:
                        gameOver2(playSurface, score1, score2)
                        game_started = False
                    if snakePosition2[1] > 460 or snakePosition2[1] < 0:
                        gameOver2(playSurface, score1, score2)
                        game_started = False
                    for snakeBody2 in snakeSegments2[1:]:  # 玩家一撞上了玩家二，玩家一失败
                        if snakePosition1[0] == snakeBody2[0] and snakePosition1[1] == snakeBody2[1]:
                            gameOver1(playSurface, chapter, [score1, score2])
                            game_started = False
                            break
                    if snakePosition1[0] == snakePosition2[0] and snakePosition1[1] == snakePosition2[1]:   # 头碰头，谁长谁赢，否则平局。
                        if len(snakeSegments1) > len(snakeSegments2):
                            gameOver2(playSurface, score1, score2)
                        elif len(snakeSegments1) < len(snakeSegments2):
                            gameOver1(playSurface, chapter, [score1, score2])
                        else:
                            gameOver(playSurface, score1, score2)
                        game_started = False
                if not game_started:
                    break

            else:  # 游戏没有开始，显示欢迎界面
                # playSurface.blit(welcome_words, (188, 100))
                # playSurface.blit(start_game_words, (236, 310))
                # playSurface.blit(close_game_words, (233, 350))
                break
            pygame.display.update()
            fpsClock.tick(5)


if __name__ == "__main__":
    main()
