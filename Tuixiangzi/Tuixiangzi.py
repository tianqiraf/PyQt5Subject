# -*- coding: utf-8 -*-
# @Author: Kali
# @Date:   2016-12-13 11:11:07
# @Last Modified by:   Marte
# @Last Modified time: 2016-12-14 10:07:41

# map
# ---------------------y
# |
# |
# |
# |
# |
# |
# |
# |
# x

import pygame
import time
import os
import random
import threading
import win32api, win32con
from pygame.locals import *
from sys import exit


# pygame初始化
pygame.init()

#全局变量的声明
#Global Vara
Game_font = pygame.font.SysFont("arial",32)
Game_Map_Source = []
Game_Step = 0
Player_Pos=[0,0]
Game_Level = 4
Game_Map = []
Map_Wide = 0
Map_Deepth = 0
Game_Path = []
Dir = ((-1,0),(1,0),(0,-1),(0,1))
BackgroundSize = 768
Game_Map_Size = 64
#Global Var Done

# 设置游戏窗口的大小
Game_Screen = pygame.display.set_mode((BackgroundSize, BackgroundSize), 0, 32)
pygame.display.set_caption("推箱子")

Image_Help          =   pygame.image.load("Tuixiangzi/source/help.png").convert()
Image_Welcome       =   pygame.image.load("Tuixiangzi/source/main.png").convert()
Image_Box_Inplace   =   pygame.image.load("Tuixiangzi/source/Box_Inplace.jpg").convert()
Image_Box_Outplace  =   pygame.image.load("Tuixiangzi/source/Box_Outplace.JPG").convert()
Game_Success        =   pygame.image.load("Tuixiangzi/source/Success.jpg").convert()
Image_Player        =   pygame.image.load("Tuixiangzi/source/people.png").convert()
Image_Goal          =   pygame.image.load("Tuixiangzi/source/Goal.jpg").convert()
Image_Wall          =   pygame.image.load("Tuixiangzi/source/wall.jpg").convert()

# 截取所需图片大小
Image_Help          =   pygame.transform.scale(Image_Help,(BackgroundSize,BackgroundSize))
Image_Welcome       =   pygame.transform.scale(Image_Welcome,(BackgroundSize,BackgroundSize))
Image_Box_Inplace   =   pygame.transform.scale(Image_Box_Inplace,(Game_Map_Size,Game_Map_Size))
Image_Box_Outplace  =   pygame.transform.scale(Image_Box_Outplace,(Game_Map_Size,Game_Map_Size))
Image_Player        =   pygame.transform.scale(Image_Player,(Game_Map_Size,Game_Map_Size))
Image_Wall          =   pygame.transform.scale(Image_Wall,(Game_Map_Size,Game_Map_Size))
Image_Goal          =   pygame.transform.scale(Image_Goal,(Game_Map_Size,Game_Map_Size))
Image_Game_Success  =   pygame.transform.scale(Game_Success,(Game_Map_Size * 2,Game_Map_Size * 2))


# 菜单进入后默认显示界面
# Defult Unit
def Defult():

    global Game_Map
    # 默认进行第一个关卡
    global Game_Level
    global Map_Wide
    global Map_Deepth
    global Game_Path
    global Game_Map_Source
    global Player_Pos
    Game_Path = []
    Game_Map = []
    Map_Reader(Game_Level)
    Game_Map_Source = Game_Map[:]
    # 显示标题
    pygame.display.set_caption("推箱子 %s   Step %s" % (str(Game_Level),str(Game_Step)))
    pygame.display.update()
    # 将关卡地图设置为图片(长度 <-> 宽度) * 地图(长度 <-> 宽度)
    return pygame.display.set_mode((Map_Wide*64,Map_Deepth*64),0,32)
# Defult Unit Done


# Read Map Unit
def Map_Reader(Mission):

    global Game_Map
    global Map_Deepth
    global Map_Wide
    try:
        File_Name ="Tuixiangzi/map/"+ str(Mission) +'.dat'
        file = open(File_Name,'r')
        # 读取地图的设置信息
        Map_Deepth,Map_Wide = map(int,file.readline().split())

        for i in range(Map_Deepth):
            Game_Map.append(file.readline()[:Map_Wide])
            # print (Game_Map.append(file.readline()[:Map_Wide]))

    except Exception as e:
        pygame.display.quit()
        exit()
        print ('恭喜您全部通关')

    finally:
         file.close()


# Read Map Unit Done



# Draw Map Unit
def Display_refresh(Game_Screen):
    global Game_Level
    global Game_Step
    global Game_Map
    global Map_Deepth
    global Map_Wide
    global Player_Pos
    # 地图例子
    # NNNWWWNNNN
    # NNNWGWNNNN
    # NNNWNWWWWN
    # NWWWBNBGWN
    # NWGNBPWWWN
    # NWWWWBWNNN
    # NNNNWGWNNN
    # NNNNWWWNNN
    Game_Screen.fill((255,255,255))
    for i in range(Map_Deepth):
        for j in range(Map_Wide):
            pos = [j*64,i*64]

            # 人物
            if Game_Map[i][j]    == 'P':
                Game_Screen.blit(Image_Player,pos)
                Player_Pos[0] = i
                Player_Pos[1] = j

            # 墙
            elif  Game_Map[i][j] == 'W':
                Game_Screen.blit(Image_Wall,pos)

            # 箱子(不在指定位置)
            elif  Game_Map[i][j] == 'B':
                Game_Screen.blit(Image_Box_Outplace,pos)

            # 箱子(在指定位置)
            elif  Game_Map[i][j] == 'A':
                Game_Screen.blit(Image_Box_Inplace,pos)

            # 需要填充的位置
            elif  Game_Map[i][j] == 'G':
                Game_Screen.blit(Image_Goal,pos)

    pygame.display.set_caption("推箱子 "+str(Game_Level))
    # Game_Screen.blit(Game_font.render("space to redo",True,(0,0,0)),(0,Map_Deepth*64-32))
    pygame.display.update()
# Draw Map Unit Done


# Check Unit
def Check_Win():
    num = 0
    global Game_Map
    global Map_Wide
    global Map_Deepth

    # 最终整个地图中 B -> A 如果遍历地图发现存在 B 说明还没有胜利
    for i in range(Map_Deepth):
        for j in range(Map_Wide):
            if Game_Map[i][j] == 'B':
                return False

    return True
# Check Win Unit


# Move Unit
def Move(dir):
    global Game_Screen
    global Game_Map
    global Player_Pos
    global Game_Step
    global Game_Path
    global Game_Map_Source
    global Map_Wide
    global Map_Deepth

    # 得出当前人物所在位置
    Player_Stand = Game_Map[Player_Pos[0]][Player_Pos[1]]

    Temp_x = Player_Pos[0] + Dir[dir][0]
    Temp_y = Player_Pos[1] + Dir[dir][1]

    # print(Player_Pos[0],Player_Pos[1])          #打印人物当前位置
    # print( Temp_x,Temp_y)                       # 移动之后的位置
    # print( Game_Map[Temp_x][Temp_y])            # 移动之后位置的地图情况

    '''
             在移动时 遇到的情况
                 1）前面是墙体 W (无须处理)                           -----> 见 @ 3
                 2）前面是箱子（A | 在指定位置  B | 不在指定位置）    -----> 见 @ 1
                 3）什么都没有 N | G                                  -----> 见 @ 2

    '''
    # If there is a Box @ 1
    if Game_Map[Temp_x][Temp_y] in ('A','B'):
        print( "there is a box")
        #  如果前面是是箱子的话，那么需要移动箱子 就会遇到两种情况
        #  N 什么都没有 G | 箱子的目标地点
        #  提前预测一下前面的情况，方可移动箱子
        if Game_Map[Temp_x + Dir[dir][0]][Temp_y + Dir[dir][1]] in ('N','G'):
            # Move Box
            Game_Path.append(Game_Map[:])

            # 如果是箱子目标的地方 那么需要将下一个地方变成 A
            if Game_Map[Temp_x + Dir[dir][0]][Temp_y + Dir[dir][1]] == 'G':
                Change_Map(Temp_x + Dir[dir][0],Temp_y + Dir[dir][1],'A')
            # 其他情况将下个位置变成箱子
            else:
                Change_Map(Temp_x + Dir[dir][0],Temp_y + Dir[dir][1],'B')

            # 设置人物当前的位置
            Change_Map(Temp_x,Temp_y,'P')

            # 设置人物之前的位置 如果是 G 依然放置 G
            if Game_Map_Source[Player_Pos[0]][Player_Pos[1]] == 'G':
                Change_Map(Player_Pos[0],Player_Pos[1],"G")
            # 如果是 N  人物走之后依然是 N
            else:
                Change_Map(Player_Pos[0],Player_Pos[1],"N")

            # 更新人物位置
            Player_Pos[0] = Temp_x
            Player_Pos[1] = Temp_y

            Display_refresh(Game_Screen)
            return

    #if there is nothing @ 2
    if Game_Map[Temp_x][Temp_y] in ("N","G"):
        print( "do it")

        # 设置人物当前的位置
        Change_Map(Temp_x,Temp_y,'P')

        # 设置人物之前的位置
        if Game_Map_Source[Player_Pos[0]][Player_Pos[1]] == 'G':
            Change_Map(Player_Pos[0],Player_Pos[1],"G")
        else:
            Change_Map(Player_Pos[0],Player_Pos[1],"N")

        #更新人物位置
        Player_Pos[0] = Temp_x
        Player_Pos[1] = Temp_y

    #else do nothing  @ 3
    Display_refresh(Game_Screen)
# Move Done


# 撤销上一次的操作
#Undo Unit
def Undo():
    global Game_Screen
    global Game_Map
    global Game_Path
    if Game_Path:
        # 取出地图所有元素
        Game_Map = Game_Path[-1][:]
        del Game_Path[-1]
        # print( Game_Map)
        Display_refresh(Game_Screen)
    else:
        print( "You can't forback")
#Undo Unit Done


# 重置本次关卡
#Redo Unit
def Redo():
    global Game_Map_Source
    global Game_Map
    global Game_Screen
    Game_Map = Game_Map_Source[:]
    Display_refresh(Game_Screen)
#Redo Done


# 更新地图信息
# Map Change Unit
def Change_Map(x,y,object):
    global Game_Map
    Game_Map[x] = Game_Map[x][:y] + object+Game_Map[x][y + 1:]
# Map Change Done


def random_move():
    global Game_Screen
    global Game_Map
    global Player_Pos
    global Game_Step
    global Game_Path
    global Game_Map_Source
    global Map_Wide
    global Map_Deepth

    i_list = []
    j_list = []
    for i in range(Map_Deepth):
        for j in range(Map_Wide):
            if Game_Map[i][j] == 'B':
                i_list.append(i)
                j_list.append(j)
                print(i,j)
    print(i_list,j_list)
    order = random.randint(1, len(j_list))
    print(order)
    Temp_x = i_list[order - 1]
    Temp_y = j_list[order - 1]
    print(Temp_x,Temp_y)
    i_list = []
    # dir = random.randint(0,3)
    # If there is a Box @ 1
    if Game_Map[Temp_x][Temp_y] == 'B':
        print("this box")
        #  N 什么都没有 G | 箱子的目标地点
        #  提前预测一下前面的情况，方可移动箱子
        for dir in range(4):
            if Game_Map[Temp_x + Dir[dir][0]][Temp_y + Dir[dir][1]] in ('N', 'G'):
                i_list.append(dir)
                print(dir)
                print(i_list)
        dir = i_list[random.randint(1, len(i_list))-1]
        print('get dir')
        if Game_Map[Temp_x + Dir[dir][0]][Temp_y + Dir[dir][1]] in ('N', 'G'):
            # Move Box
            print('really move')
            Game_Path.append(Game_Map[:])

            # 如果是箱子目标的地方 那么需要将下一个地方变成 A
            if Game_Map[Temp_x + Dir[dir][0]][Temp_y + Dir[dir][1]] == 'G':
                Change_Map(Temp_x + Dir[dir][0], Temp_y + Dir[dir][1], 'A')
            # 其他情况将下个位置变成箱子
            else:
                Change_Map(Temp_x + Dir[dir][0], Temp_y + Dir[dir][1], 'B')

            Change_Map(Temp_x, Temp_y, 'N')

            Display_refresh(Game_Screen)



# 设置函数的入口点
# main function entry point Unit
if __name__ == "__main__":
    Game_Screen.blit(Image_Welcome,(0,0))
    pygame.display.update()
    flag = True
    fileNumber = 0

    # 获取关卡数
    for filename in os.listdir(r'Tuixiangzi/map/'):
        fileNumber = fileNumber + 1

    # 加载背景音乐
    #filename = r'source/4085.wav'
    #pygame.mixer.music.load(filename)
    #pygame.mixer.music.play(loops = 0, start = 0.0)

    while flag:
        Game_Screen.blit(Image_Welcome,(0,0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.display.quit()
                exit()
            if event.type == KEYDOWN:                   #数字1
                if event.key == 49:
                    flag = False
                    break
                if event.key == 50:                     #数字2
                    Game_Screen.blit(Image_Help,(0,0))
                    pygame.display.update()
                    time.sleep(3)
                if event.key == 51:                     #数字3
                    pygame.display.quit()
                    exit()
    Game_Screen = Defult()
    Display_refresh(Game_Screen)

    #print(Player_Pos)
    #print(Game_Map)

    # 按键处理程序
    while True:
        for event in pygame.event.get():
            if event.type      == KEYDOWN:
                if random.randint(0,1)>0:
                    print('move')
                    random_move()
                # 向上
                if event.key   == K_UP:
                    Move(0)
                # 向下
                elif event.key == K_DOWN:
                    Move(1)
                # 向左
                elif event.key == K_LEFT:
                    Move(2)
                # 向右
                elif event.key == K_RIGHT:
                    Move(3)
                # 撤销
                elif event.key == K_r:
                    Undo()
                # 重置
                elif event.key == K_SPACE:
                    Redo()
                # 退出
                elif event.key == K_q:
                    pygame.display.quit()
                    exit()
            elif event.type == QUIT:
                pygame.display.quit()
                exit()
        # 如果当前关卡获胜，那么进行加载下一个关卡地图
        if (Check_Win()):
            #print( "you win")
            if Game_Level < fileNumber:
                win32api.MessageBox(0, "通关成功！即将进入下一关...", "成功", win32con.MB_OK)
                Game_Level += 1
                Defult()
                Display_refresh(Game_Screen)
            else:
                #Game_Screen = pygame.display.set_mode((572,416),0,32)
                # 将当前图片显示在窗体中心位置
                Game_Screen.blit(Image_Game_Success,(300 - 128/2,300 - 128/2))
                pygame.display.update()

# main function entry point Done


