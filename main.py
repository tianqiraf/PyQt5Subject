# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file '总设计.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import sys
import os
import requests
import sqlite3
from bs4 import BeautifulSoup
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from MainDesign import Ui_MdiArea


class MyPyQT_Form(QtWidgets.QWidget, Ui_MdiArea):
    def __init__(self):
        super(MyPyQT_Form, self).__init__()
        self.setupUi(self)
        self.book = {}
        self.chapter = {}
        self.contain = ''
        self.Book = [self.Book0, self.Book1, self.Book2, self.Book3, self.Book4,
                     self.Book5, self.Book6, self.Book7, self.Book8, self.Book9, ]
        self.dbname = "Sql.db"
        self.userdata = []
        self.alldata = []
        self.gamelist = ['tanchishe', 'tuixiangzi', 'eluosi', 'feijida']
        self.dblist = ['id', 'username', 'userpassword', 'usernickname', 'usersex', 'userage', 'jingyan', 'lv',
                       'favorite', 'tanchishe', 'tuixiangzi', 'eluosi', 'dafeiji',
                       'tanchishescore', 'tuixiangziscore', 'eluosiscore', 'dafeijiscore']
        self.conn = sqlite3.connect(self.dbname)
        self.cursor = self.conn.cursor()

        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap("./icon/bg_1.jpg")))

        self.LoginWindow.setPalette(window_pale)
        self.MainWindow.setPalette(window_pale)
        self.BookWindow.setPalette(window_pale)
        self.GameWindow.setPalette(window_pale)
        self.RegisterWindow.setPalette(window_pale)
        self.ContainWindow.setPalette(window_pale)
        self.CelueWindow.setPalette(window_pale)
        self.ZongheWindow.setPalette(window_pale)
        self.YizhiWindow.setPalette(window_pale)
        self.DuizhanWindow.setPalette(window_pale)
        self.PaihangWindow.setPalette(window_pale)
        self.MainWindow.setFixedSize(900, 540)
        self.BookWindow.setFixedSize(900, 540)
        self.GameWindow.setFixedSize(900, 540)
        self.LoginWindow.setFixedSize(480, 280)
        self.RegisterWindow.setFixedSize(360, 480)
        self.ContainWindow.setFixedSize(1200, 800)
        self.CelueWindow.setFixedSize(900, 540)
        self.ZongheWindow.setFixedSize(900, 540)
        self.YizhiWindow.setFixedSize(900, 540)
        self.DuizhanWindow.setFixedSize(900, 540)

    def login(self):
        username = self.UserNameInput.text()
        userpassword = self.UserPaswordInput.text()
        # 没有输入用户名
        if not username:
            # 弹窗提醒
            reply = QMessageBox.information(self, '登陆失败', '请输入账号！', QMessageBox.Ok)
            return
        # 没有输入密码
        if not userpassword:
            reply = QMessageBox.information(self, '登陆失败', '请输入密码！', QMessageBox.Ok)
            return
        # 从数据库检索是否有该用户名
        self.userdata = self.cursor.execute("select * from user where username='%s'" % username).fetchone()
        # 如果有
        if self.userdata:
            self.userdata = list(self.userdata)
            # 检测密码是否正确
            if self.userdata[2] == userpassword:
                reply = QMessageBox.information(self, '登陆成功', '登陆成功！', QMessageBox.Ok)
                # 经验+1
                self.userdata[6] += 1
                print(self.userdata[6])
                # 写入增加后的经验值以及用户等级，获取等级使用get_level()
                self.cursor.execute("update user set jingyan = %d ,lv = %d where id = %d" % (
                                self.userdata[6], get_level(self.userdata[6]), self.userdata[0]))
                # 提交数据库修改
                self.conn.commit()
                # 显示等级
                self.LvNum.display(get_level(self.userdata[6]))
                print(self.userdata[3])
                # 欢迎语
                self.WelcomeAndName.setText(
                    "<html><head/><body><p><span style=' font-size:16pt;'>{},欢迎登录！</span></p></body></html>".format(
                        self.userdata[3]))
                # 隐藏登陆窗口，显示主窗口
                self.LoginWindow.hide()
                self.MainWindow.show()
                self.MainWindow.raise_()
            # 密码不正确
            else:
                reply = QMessageBox.information(self, '登陆失败', '密码错误，请重新输入！', QMessageBox.Ok)
                self.UserPaswordInput.setText("")
        # 数据库中无该用户名
        else:
            reply = QMessageBox.information(self, '登陆失败', '用户名不存在，请先注册！', QMessageBox.Ok)

    def register(self):
        # 得到用户输入的帐号，密码，昵称,性别，年龄
        username = self.RegisterUserNameInput.text()
        userpassword = self.RegisterUserPasswordInput.text()
        usernickname = self.RegisterUserNickNameInput.text()
        usersex = 'man' if self.RegisterUserSexManInput.isChecked() else 'woman'
        userage = self.RegisterUserAgeInput.value()
        # 有部分信息未填
        if not username or not userpassword or not usernickname or not usersex or not userage:
            reply = QMessageBox.information(self, '注册失败', '请将信息填写完整！', QMessageBox.Ok)
            return

        # 检测帐号重复
        data = self.cursor.execute("select * from user where username='%s'" % username).fetchone()
        if data:
            reply = QMessageBox.information(self, '注册失败', '账号已存在，请重新输入！', QMessageBox.Ok)
            return
        # 检测昵称重复
        data = self.cursor.execute("select * from user where usernickname='%s'" % usernickname).fetchone()
        if data:
            reply = QMessageBox.information(self, '注册失败', '昵称已存在，请重新输入！', QMessageBox.Ok)
            return

        print(username, userpassword, usernickname, userage, usersex, userage, type(userage))
        # 数据库ID自增
        id = self.cursor.execute("select count(*) from user").fetchone()[0] + 1
        # 写入用户信息到数据库
        self.cursor.execute("insert into user values(%d, '%s', '%s', '%s', '%s', %d, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0);"
                            % (id, username, userpassword, usernickname, usersex, userage))
        # 提交数据库改动
        self.conn.commit()
        reply = QMessageBox.information(self, '注册成功', '注册成功！请登陆', QMessageBox.Ok)
        # 注册成功自动隐藏注册窗口，显示登陆窗口
        self.RegisterWindow.hide()
        self.LoginWindow.show()

    def sex_choosed(self):
        self.RegisterUserSexWomanInput.setChecked(not self.RegisterUserSexManInput.isChecked())
        self.RegisterUserSexManInput.setChecked(not self.RegisterUserSexWomanInput.isChecked())

    def go_to_register(self):
        # 隐藏登陆窗口
        self.LoginWindow.hide()
        # 注册窗口各文本框控件置空
        self.RegisterUserNameInput.setText('')
        self.RegisterUserPasswordInput.setText('')
        self.RegisterUserNickNameInput.setText('')
        # 显示注册窗口
        self.RegisterWindow.show()
        # 将注册窗口显示在最上层
        self.RegisterWindow.raise_()

    def book_click(self):
        # 得到书籍排行榜
        self.book = get_rank()
        # 显示书籍标题信息
        for i in range(0, len(self.Book)):
            self.Book[i].setText(self.book['name'][i] + '--------' + self.book['author'][i])
        # 隐藏主窗口，显示书籍窗口
        self.MainWindow.hide()
        self.BookWindow.show()
        self.BookWindow.raise_()

    def game_click(self):
        # 隐藏主窗口，显示游戏窗口
        self.MainWindow.hide()
        self.GameWindow.show()
        self.GameWindow.raise_()

    def yizhi_click(self):
        # 隐藏游戏窗口，显示益智游戏分类
        self.GameWindow.hide()
        self.YizhiWindow.show()
        self.YizhiWindow.raise_()

    def celue_click(self):
        # 隐藏游戏窗口，显示策略游戏分类
        self.GameWindow.hide()
        self.CelueWindow.show()
        self.CelueWindow.raise_()

    def duizhan_click(self):
        # 隐藏游戏窗口，显示对战游戏分类
        self.GameWindow.hide()
        self.DuizhanWindow.show()
        self.DuizhanWindow.raise_()

    def zonghe_click(self):
        # 隐藏游戏窗口，显示综合游戏分类
        self.GameWindow.hide()
        self.ZongheWindow.show()
        self.ZongheWindow.raise_()

    def yizhipaihang_click(self):
        pass

    def celuepaihang_click(self):
        self.alldata = self.cursor.execute("select * from user").fetchall()
        celue_paihang = {}
        for i in range(len(self.alldata)):
            celue_paihang[self.alldata[i][3]] = self.alldata[i][15]
        celue = sorted(celue_paihang.items(), key=lambda item: int(item[1]), reverse=True)
        self.Name_1.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        celue[0][0]))
        self.Score_1.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        celue[0][1]))
        self.Name_2.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        celue[1][0]))
        self.Score_2.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        celue[1][1]))
        self.Name_3.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        celue[2][0]))
        self.Score_3.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        celue[2][1]))
        self.Name_4.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        celue[3][0]))
        self.Score_4.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        celue[3][1]))
        self.Name_5.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        celue[4][0]))
        self.Score_5.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        celue[4][1]))
        self.PaihangName.setText("俄罗斯方块")
        self.PaihangWindow.show()

    def zonghepaihang_click(self):
        self.alldata = self.cursor.execute("select * from user").fetchall()
        zonghe_paihang = {}
        for i in range(len(self.alldata)):
            zonghe_paihang[self.alldata[i][3]] = self.alldata[i][16]
        print(zonghe_paihang)
        zonghe = sorted(zonghe_paihang.items(), key=lambda item: int(item[1]), reverse=True)
        self.Name_1.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        zonghe[0][0]))
        self.Score_1.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        zonghe[0][1]))
        self.Name_2.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        zonghe[1][0]))
        self.Score_2.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        zonghe[1][1]))
        self.Name_3.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        zonghe[2][0]))
        self.Score_3.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        zonghe[2][1]))
        self.Name_4.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        zonghe[3][0]))
        self.Score_4.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        zonghe[3][1]))
        self.Name_5.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        zonghe[4][0]))
        self.Score_5.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        zonghe[4][1]))
        self.PaihangName.setText("飞机大战")
        self.PaihangWindow.show()

    def duizhanpaihang_click(self):
        # 获取数据库中所有用户数据
        self.alldata = self.cursor.execute("select * from user").fetchall()
        duizhan_paihang = {}
        # 获取所有用户的贪吃蛇分数
        for i in range(len(self.alldata)):
            duizhan_paihang[self.alldata[i][3]] = self.alldata[i][13]
        # 按分数排序
        duizhan = sorted(duizhan_paihang.items(), key=lambda item: int(item[1]), reverse=True)
        # 显示前五名用户及分数
        self.Name_1.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        duizhan[0][0]))
        self.Score_1.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        duizhan[0][1]))
        self.Name_2.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        duizhan[1][0]))
        self.Score_2.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        duizhan[1][1]))
        self.Name_3.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        duizhan[2][0]))
        self.Score_3.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        duizhan[2][1]))
        self.Name_4.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        duizhan[3][0]))
        self.Score_4.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        duizhan[3][1]))
        self.Name_5.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        duizhan[4][0]))
        self.Score_5.setText("<html><head/><body><p><span style=' font-size:23pt;'>{}</span></p></body></html>".format(
                        duizhan[4][1]))
        self.PaihangName.setText("贪吃蛇")
        self.PaihangWindow.show()

    def tanchishe_click(self):
        # 贪吃蛇玩的次数+1
        self.userdata[9] += 1
        # 写入数据库
        self.cursor.execute("update user set tanchishe = %d, favorite = '%s' where id = %d" % (
                self.userdata[9], self.gamelist[self.userdata[9:13].index(max(self.userdata[9:13]))], self.userdata[0]))
        # 提交数据库改动
        self.conn.commit()
        # 隐藏当前窗口
        self.DuizhanWindow.hide()
        # 打开贪吃蛇游戏
        os.system("python Tanchishe/Tanchishe.py")
        # 贪吃蛇游戏运行结束
        # score.dat记录了分数
        filename = './Tanchishe/score.dat'
        # 存在文件则打开读取分数
        if os.path.isfile(filename):
            fp = open(filename, 'r')
            score = fp.read()
            fp.close()
        # 不存在则分数为0
        else:
            score = '0'
        # 贪吃蛇的分数
        self.userdata[13] = int(score)
        # 分数写入数据库
        self.cursor.execute("update user set tanchishescore = %d where id = %d" % (self.userdata[13], self.userdata[0]))
        self.conn.commit()
        # 显示对战游戏窗口
        self.DuizhanWindow.show()
        self.DuizhanWindow.raise_()

    def tuixiangzi_click(self):
        # 推箱子次数+1
        self.userdata[10] += 1
        self.cursor.execute("update user set tuixiangzi = %d, favorite = %s where id = %d" % (
                self.userdata[10], self.gamelist[self.userdata[9:13].index(max(self.userdata[9:13]))], self.userdata[0]))
        self.conn.commit()

        self.YizhiWindow.hide()
        os.system("python Tuixiangzi/Tuixiangzi.py")

        self.YizhiWindow.show()
        self.YizhiWindow.raise_()

    def eluosi_click(self):
        # 俄罗斯方块次数+1
        self.userdata[11] += 1
        self.cursor.execute("update user set eluosi = %d, favorite = %s where id = %d" % (
                self.userdata[11], self.gamelist[self.userdata[9:13].index(max(self.userdata[9:13]))], self.userdata[0]))
        self.conn.commit()

        self.CelueWindow.hide()
        os.system("python Eluosi/Eluosi.py")

        filename = './Eluosi/score.dat'
        if os.path.isfile(filename):
            fp = open(filename, 'r')
            score = fp.read()
            fp.close()
        else:
            score = '0'
        self.userdata[15] = int(score)  # 俄罗斯方块分数
        self.cursor.execute("update user set eluosiscore = %d where id = %d" % (self.userdata[15], self.userdata[0]))
        self.conn.commit()

        self.CelueWindow.show()
        self.CelueWindow.raise_()

    def feijida_click(self):
        self.userdata[12] += 1  # 飞机大战次数+1
        self.cursor.execute("update user set feijida = %d, favorite = %s where id = %d" % (
                self.userdata[12], self.gamelist[self.userdata[9:13].index(max(self.userdata[9:13]))], self.userdata[0]))
        self.conn.commit()

        self.ZongheWindow.hide()
        os.system("python Feijidazhan/Feijidazhan.py")

        filename = './Feijidazhan/score.dat'
        if os.path.isfile(filename):
            fp = open(filename, 'r')
            score = fp.read()
            print('read score:', score)
            fp.close()
        else:
            score = '0'
        print('score:', score)
        self.userdata[16] = int(score)  # 飞机大战分数
        self.cursor.execute("update user set feijidascore = %d where id = %d" % (self.userdata[16], self.userdata[0]))
        self.conn.commit()

        self.ZongheWindow.show()
        self.ZongheWindow.raise_()

    def book_rank_click(self):
        # 得到点击的按钮对应的书名
        index = self.Book.index(self.sender())
        # 通过书名获得各个章节的信息
        self.chapter = get_chapter(self.book['url'][index])
        # 获取当前章节的内容
        self.contain = get_contain(self.chapter['url'][index])
        # 以书名作为窗口标题
        self.ContainWindow.setWindowTitle(self.book['name'][index])
        # 显示书名以及作者
        self.BookName.setText(self.book['name'][index] + "\n                  --------" + self.book['author'][index])
        # 断开之前绑定的槽函数连接
        self.Chapter.currentIndexChanged['QString'].disconnect(self.choose_chapter)
        # 清除ComboBox选项（章节名称）
        self.Chapter.clear()
        # 添加ComboBox选项（章节名称）
        for i in range(len(self.chapter['chapter'])):
            self.Chapter.addItem(self.chapter['chapter'][i])
        # 建立槽函数连接
        self.Chapter.currentIndexChanged['QString'].connect(self.choose_chapter)
        # 显示当前章节的内容
        self.BookContain.setText(self.contain)
        # 隐藏名著阅读窗口
        self.BookWindow.hide()
        # 显示书籍详情窗口
        self.ContainWindow.show()
        self.ContainWindow.raise_()

    def book_back_click(self):
        self.BookWindow.hide()
        self.MainWindow.show()
        self.MainWindow.raise_()

    def game_back_click(self):
        self.GameWindow.hide()
        self.MainWindow.show()
        self.MainWindow.raise_()

    def contain_back_click(self):
        self.ContainWindow.hide()
        self.BookWindow.show()
        self.BookWindow.raise_()

    def paihang_back_click(self):
        self.PaihangWindow.hide()

    def game_detail_back(self):
        self.CelueWindow.hide()
        self.ZongheWindow.hide()
        self.DuizhanWindow.hide()
        self.YizhiWindow.hide()
        self.GameWindow.show()
        self.GameWindow.raise_()

    def back_to_login(self):
        self.RegisterWindow.hide()
        self.LoginWindow.show()
        self.LoginWindow.raise_()

    # 选择ComboBox章节
    def choose_chapter(self):
        # 获取选择的章节
        choose = self.Chapter.currentIndex()
        # 显示在QTextBrowser中
        self.BookContain.setPlainText(get_contain(self.chapter['url'][choose]))

    def coding(self):
        reply = QMessageBox.information(self, '请稍等', '功能开发中...', QMessageBox.Ok)


# 得到书籍排名
def get_rank():
    print("get rank")
    response = s.get('https://mingzhu.zbyw.cn/')
    # 设置编码方式utf-8，否则会乱码
    response.encoding = 'utf-8'
    # BeautifulSoup来处理html文本
    soup = BeautifulSoup(response.text, 'html.parser')
    # 书籍信息，包括名称，链接，作者
    book = {'name': [], 'url': [], 'author': []}
    # 筛选有用的标签
    allbook = soup.find_all(class_='topic_feature')
    # 获取10本书籍信息
    for i in range(10):
        book['name'].append(allbook[i].p.a.string)
        book['url'].append("https://mingzhu.zbyw.cn" + allbook[i].p.a['href'])
        book['author'].append(allbook[i].div.p.string)
    print("get rank OK")
    return book


# 得到书籍的所有章节
def get_chapter(url):
    print("get chapter")
    # 通过书籍链接获取到所有章节
    response = s.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    tmp_chapter = soup.find_all(class_='sub_list_twono')[0].ul.find_all("li")
    chapter_num = []
    chapter_url = []
    for i in range(len(tmp_chapter)):
        chapter_num.append(tmp_chapter[i].a.text)
        chapter_url.append("https://mingzhu.zbyw.cn" + tmp_chapter[i].a['href'])
    chapter = {}
    # 这个字典存储了书籍的所有章节以及对应的链接
    chapter['chapter'] = chapter_num
    chapter['url'] = chapter_url
    print("get chapter OK")
    return chapter


# 得到书籍章节的内容
def get_contain(url):
    print("get contain")
    # 通过书籍章节的链接获取到章节内容
    response = s.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    # tmp_contain就是章节内容
    tmp_contain = soup.find(class_='mzcon')
    # 去除文中的链接（<a>标签）
    [s.extract() for s in tmp_contain('a')]
    print("get contain OK")
    return tmp_contain


def get_level(jingyan):
    for i in range(1, 99):
        if 5 * i * (i - 1) / 2 <= jingyan < 5 * i * (i + 1) / 2:
            return i
    return 0


if __name__ == '__main__':
    s = requests.Session()
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.LoginWindow.show()
    sys.exit(app.exec_())
