# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 14:20:11 2019
@author: Raf
"""
import copy
import pygame
import random
import win32api, win32con
import os
from pygame.locals import *

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


class block:
    def __init__(self):
        pygame.init()
        self.x = random.randint(1, W-3)
        self.y = 0
        self.rects = []
        self.rect_one = []
        self.rect_two = []
        self.rect_three = []
        self.rect_four = []
        self.teg = 1
        self.model = 0
        # 是否到达底部
        self.bottom = False

    def get_model(self, model):
        self.model = model
        if model == 1:
            self.rect_one =[self.x, self.y]
            self.rect_two =[self.x, self.y + 1]
            self.rect_three =[self.x + 1, self.y]
            self.rect_four =[self.x + 1, self.y + 1]
            # self.rects = [[self.x, self.y], [self.x, self.y + 1], [self.x + 1, self.y], [self.x + 1, self.y + 1]]
        elif model == 2:
            self.rect_one =[self.x, self.y]
            self.rect_two =[self.x + 1, self.y]
            self.rect_three =[self.x + 1, self.y + 1]
            self.rect_four = [self.x + 2, self.y + 1]
            #  self.rects = [[self.x, self.y], [self.x + 1, self.y], [self.x + 1, self.y + 1], [self.x + 2, self.y + 1]]
        elif model == 3:
            self.rect_one =[self.x, self.y]
            self.rect_two =[self.x + 1, self.y]
            self.rect_three =[self.x - 1, self.y + 1]
            self.rect_four = [self.x, self.y + 1]
            # self.rects = [[self.x, self.y], [self.x + 1, self.y], [self.x - 1, self.y + 1], [self.x, self.y + 1]]
        elif model == 4:
            self.rect_one =[self.x, self.y]
            self.rect_two = [self.x, self.y + 1]
            self.rect_three = [self.x, self.y + 2]
            self.rect_four =[self.x + 1, self.y + 2]
            # self.rects = [[self.x, self.y], [self.x, self.y + 1], [self.x, self.y + 2], [self.x + 1, self.y + 2]]
        elif model == 5:
            self.rect_one =[self.x, self.y]
            self.rect_two =[self.x, self.y + 1]
            self.rect_three =[self.x, self.y + 2]
            self.rect_four =[self.x - 1, self.y + 2]
            #   self.rects = [[self.x, self.y], [self.x, self.y + 1], [self.x, self.y + 2], [self.x - 1, self.y + 2]]
        elif model == 6:
            self.rect_one =[self.x, self.y]
            self.rect_two =[self.x, self.y + 1]
            self.rect_three =[self.x, self.y + 2]
            self.rect_four =[self.x, self.y + 3]
            #  self.rects = [[self.x, self.y], [self.x, self.y + 1], [self.x, self.y + 2], [self.x, self.y + 3]]
        elif model == 7:
            self.rect_one =[self.x, self.y]
            self.rect_two =[self.x - 1, self.y + 1]
            self.rect_three =[self.x, self.y + 1]
            self.rect_four =[self.x + 1, self.y + 1]
            # self.rects = [[self.x, self.y], [self.x - 1, self.y + 1], [self.x, self.y + 1], [self.x + 1, self.y + 1]]
        
        self.tag = 1
        self.rects = [self.rect_one, self.rect_two, self.rect_three, self.rect_four]
        
    def down(self):

        # 判断下方是否为墙壁
        for rect in self.rects:
            if rect[1] == H - 1:
                self.bottom = True
                break
            for wallrect in wall:
                if rect[0] == wallrect[0] and rect[1] == wallrect[1]-1:
                    self.bottom = True
                    break
        # 如果下方是墙壁，则说明方块已经到达底部
        if self.bottom == True:
            for rect in block1.rects:
                wall.append(rect)
        # 如果没有到达底部，则继续增加
        else:
            for rect in self.rects:
                rect[1] = rect[1] + 1
                pass
            
    # 移动
    def move(self,direct):
        # 是否可以左右移动
        self.leftmove = True
        self.rightmove = True

        for rect in self.rects:
            for wallrect in wall:
                if rect[0] == wallrect[0] - 1 and rect[1] == wallrect[1]:
                    self.rightmove = False
                elif rect[0] == wallrect[0] + 1 and rect[1] == wallrect[1]:
                    self.leftmove = False
        for rect in self.rects:
            if rect[0] >= W-1:
                self.rightmove = False
            if rect[0] <= 0:
                self.leftmove = False
        if direct == 'left' and self.leftmove == True :
            for rect in self.rects:
                rect[0] = rect[0] - 1
        elif direct == 'right' and self.rightmove == True :
            for rect in self.rects:
                rect[0] = rect[0] + 1

    # 判断旋转撞墙
    def rotateinwall(self):

        bl = False
        br = False
        for rect in self.rects:
            if rect[0]<0:
                bl = True
            elif rect[0]>W-1:
                br = True
        if bl:
            for rect in self.rects:
                rect[0]+=1
        elif br:
            for rect in self.rects:
                rect[0]-=1
        # 此处判断是否撞击已为墙壁方块
        flag = False
        for rect in self.rects:
            for wallrect in wall:
                if rect == wallrect:
                    flag = True
        return flag

    # 进墙后操作
    def rotatemove(self,oldself,oldtag):
        inwall = True
        flag = 0
        # 以一号方块为中心移动至周围九宫格来判断是否有合适位置。
        while inwall:
            if (flag == 0):
                for rect in self.rects:
                    rect[0] = rect[0] - 1
                    rect[1] = rect[1] - 1
            elif(flag < 3):
                for rect in self.rects:
                    rect[0] = rect[0] +1
            elif(flag == 3):
                for rect in self.rects:
                    rect[0] = rect[0] - 2
                    rect[1]=rect[1]+1
            elif(flag < 6):
                for rect in self.rects:
                    rect[0] = rect[0] +1
            elif(flag == 6):
                for rect in self.rects:
                    rect[0] = rect[0] - 2
                    rect[1]=rect[1]+1
            elif(flag < 9):
                for rect in self.rects:
                    rect[0] = rect[0] +1
                flag=flag+1
            else:
                # 九宫格没有合适位置
                self.rects =list(oldself)
                self.tag = oldtag
                print("无位置")
                print(oldself)
                print(self.rects)
                break
                pass
            inwall= self.rotateinwall()
            flag = flag + 1
        pass
    
    # 旋转
    def rotate(self):
        oldself = copy.deepcopy(self.rects)
        #  print("当前方块")
        #  print(oldself)

        oldtag = self.tag
        if self.model == 2:
            if self.tag == 1:
                self.rect_one[0]+=2
                self.rect_one[1]-=1
                self.rect_four[1]-=1
                # a = [self.rect_one]
                self.tag = 2
            elif self.tag == 2:
                self.rect_one[0]-=2
                self.rect_one[1]+=1
                self.rect_four[1]+=1
                self.tag = 1
            pass
        elif self.model == 3:
            if self.tag == 1:
                self.rect_two[0]-=2
                self.rect_two[1]-=1
                self.rect_three[1]-=1
                #a = [self.rect_one]
                self.tag = 2
            elif self.tag == 2:
                self.rect_two[0]+=2
                self.rect_two[1]+=1
                self.rect_three[1]+=1
                self.tag = 1
        elif self.model == 4:
            if self.tag == 1:
                self.rect_three[0]+=1
                self.rect_three[1]-=2
                self.rect_four[0]+=1
                self.rect_four[1]-=2
                #a = [self.rect_one]
                self.tag = 2
            elif self.tag == 2:
                self.rect_three[0]-=2
                self.rect_three[1]-=1
                self.rect_four[0]-=2
                self.rect_four[1]-=1
                self.tag = 3
            elif self.tag == 3:
                self.rect_three[0]-=1
                self.rect_three[1]+=2
                self.rect_four[0]-=1
                self.rect_four[1]+=2
                self.tag = 4
            elif self.tag == 4:
                self.rect_three[0]+=2
                self.rect_three[1]+=1
                self.rect_four[0]+=2
                self.rect_four[1]+=1
                self.tag = 1
        elif self.model == 5:
            if self.tag == 1:
                self.rect_three[0]+=2
                self.rect_three[1]-=1
                self.rect_four[0]+=2
                self.rect_four[1]-=1
                #a = [self.rect_one]
                self.tag = 2
            elif self.tag == 2:
                self.rect_three[0]-=1
                self.rect_three[1]-=2
                self.rect_four[0]-=1
                self.rect_four[1]-=2
                self.tag = 3
            elif self.tag == 3:
                self.rect_three[0]-=2
                self.rect_three[1]+=1
                self.rect_four[0]-=2
                self.rect_four[1]+=1
                self.tag = 4
            elif self.tag == 4:
                self.rect_three[0]+=1
                self.rect_three[1]+=2
                self.rect_four[0]+=1
                self.rect_four[1]+=2
                self.tag = 1
        elif self.model == 6:
            if self.tag == 1:
                self.rect_one[0]-=1
                self.rect_one[1]+=1
                self.rect_three[0]+=1
                self.rect_three[1]-=1
                self.rect_four[0]+=2
                self.rect_four[1]-=2
                #a = [self.rect_one]
                self.tag = 2
            elif self.tag == 2:
                self.rect_one[0]+=1
                self.rect_one[1]-=1
                self.rect_three[0]-=1
                self.rect_three[1]+=1
                self.rect_four[0]-=2
                self.rect_four[1]+=2
                self.tag = 1
        elif self.model == 7:
            if self.tag == 1:
                self.rect_two[0] += 1
                self.rect_two[1] += 1
                #a = [self.rect_one]
                self.tag = 2
            elif self.tag == 2:
                self.rect_two[0] -= 1
                self.rect_two[1] -= 1
                self.rect_one[1] += 2
                self.tag = 3
            elif self.tag == 3:
                self.rect_two[0] += 2
                self.rect_two[1] += 1
                self.rect_one[0] += 1
                self.rect_one[1] -= 2
                self.tag = 4
            elif self.tag == 4:
                self.rect_two[0] -= 2
                self.rect_two[1] -= 1
                self.rect_one[0] -= 1
                self.tag = 1
        print("front")
        print(oldself)
        if self.rotateinwall():
            self.rotatemove(oldself,oldtag)

def drawrect(id = []):
    x = id[0]
    y = id[1]
    pygame.draw.rect(screen, Color, (x*SIZE, y*SIZE, SIZE - 1, SIZE - 1))
    pass


def flu() -> object:
    # 画背景墙
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, W * SIZE, H * SIZE), 0)
    # 画墙上方块
    for rect in wall:
        drawrect(rect)
    # 画空中方块
    for rect in block1.rects:
        drawrect(rect)
    pygame.display.update()


def kill():
    global score
    for i in range(0, H):
        b = True # b 记录是否应该kill某列
        a = 0 # a 记录要kill的列数
        for j in range(0, W):
            # for rect in wall:
             lit = [j, i]
             if not (lit in wall):
                b = False
        if b:
            score += 1
            for j in range(0,W):
                wall.remove([j,i])
            # 上面移除一行
            # 下面消除使上方向下一格
            for col in range(0,W):
                for row in range (i,0,-1):
                    for rect in wall:
                       if rect[0] == col and rect[1] == row:
                           rect[1] += 1

    for i in range(0, W):
        if [i, 0] in wall:
            win32api.MessageBox(0, "游戏结束！\n你的得分为：%d" % score, "游戏结束", win32con.MB_OK)
            recordScore(score)
            return True
    return False


def recordScore(score):
    filename = './Eluosi/score.dat'
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

while True:
    SIZE = 30
    H = 20
    W = 10
    Color = (125, 125, 125)

    screen = pygame.display.set_mode((W * SIZE, H * SIZE))
    pygame.display.set_caption("俄罗斯方块")
    clock = pygame.time.Clock()

    # 选择关卡界面图片
    choosechapter = pygame.image.load("./Eluosi/ChooseChapter.png")

    # 绘制背景图片
    screen.blit(choosechapter, (0, 0))

    # “开始”按钮
    buttonc1 = Button('./Eluosi/GameStartUp.png', './Eluosi/GameStartDown.png', (150,300))

    while True:

        chapter = showChapterInterface(screen, buttonc1) - 1
        if chapter == -1:
            pygame.display.update()
            continue

        score = 0
        # 方块大小及数量颜色
        speed_range = 0
        pygame.display.flip()
        wall = []
        speedlev = 40

        block1 = block()
        # block1.get_model(5)
        block1.get_model(random.randint(1, 7))
        downable = 0


        screen = pygame.display.set_mode((450, 600))
        screen.fill((255, 255, 255))
        pygame.draw.line(screen, (0, 0, 0), (300, 20), (300, 580), 4)

        text_format = pygame.font.SysFont("simsunnsimsun", 30).render("速度调节", 1, (0, 0, 0))
        screen.blit(text_format, (320, 150))
        text_format = pygame.font.SysFont("simsunnsimsun", 30).render("   %d" % ((speed_range + 60)/10), 1, (0, 0, 0))
        screen.blit(text_format, (320, 200))
        speed_add = Button('./Eluosi/SpeedAddUp.png', './Eluosi/SpeedAddDown.png', (377, 300))
        speed_subtract = Button('./Eluosi/SpeedSubtractUp.png', './Eluosi/SpeedSubtractDown.png', (377, 350))
        speed_add.show(screen)
        speed_subtract.show(screen)
        while True:
            exit_flag = False
            # 实时按钮动态
            speed_add.show(screen)
            speed_subtract.show(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in (K_ESCAPE, K_q):
                        exit_flag = True
                        break
                    elif event.key == pygame.K_LEFT:
                        block1.move('left')
                    elif event.key == pygame.K_RIGHT:
                        block1.move('right')
                    elif event.key == pygame.K_UP:
                        block1.rotate()
                    elif event.key == pygame.K_DOWN:
                        speedlev = 10
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        speedlev = 40
                elif event.type == MOUSEBUTTONDOWN:
                    if speed_add.inButtonRange() or speed_subtract.inButtonRange():
                        if speed_add.inButtonRange():
                            speed_range += 10 if speed_range<=200 else 50
                        elif speed_subtract.inButtonRange():
                            if speed_range + 50 > 0:
                                speed_range -= 10
                        # 刷新速度显示
                        screen.fill((255, 255, 255), pygame.Rect(320, 100, 350, 180))
                        text_format = pygame.font.SysFont("simsunnsimsun", 30).render("速度调节", 1, (0, 0, 0))
                        screen.blit(text_format, (320, 150))
                        text_format = pygame.font.SysFont("simsunnsimsun", 30).render(
                            "   %d" % ((speed_range + 60) / 10), 1,
                            (0, 0, 0))
                        screen.blit(text_format, (320, 200))

                pass
            downable = downable + 1
        # 判断落到底部或墙上
            if not block1.bottom:
                if downable >= speedlev:
                    block1.down()
                    downable = 0
            else:
                if kill():
                    exit_flag = True
                    break
        #生成新的牌子
                block1 = block()
                # block1.get_model(1)
                block1.get_model(random.randint(1, 7))
            flu()
            clock.tick(60 + speed_range)
            if exit_flag:
                break
        break