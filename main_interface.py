# -*- codeing = utf-8 -*-
# @Time :2021/5/18 21:08
# @Author : 刘念卿
# @File : main_interface.py
# @Software : PyCharm
import tkinter
from tkinter.scrolledtext import ScrolledText
import tkinter as tk
import base64#要将编码之后的图片数据解码并保存为图片
import os#我们删除图片，这个要添加进来
from kill import kill
from PIL import Image, ImageTk
from bg_bg_gif import img as socket_one     #接下来就是在文件中导入你刚刚生成的xxx.py文件，因为每个图片文件里面都是img变量，所以导入的时候可以用别名，这是python的基本用法了，不再多说。
from C45.C45 import main_c45
from ID3.ID3 import main_ID3
from CART.CART import main_CART
from knn.knn_1 import main_knn
from NaïveBayes.NaïveBayes import main_na
def host():
    tmp = open('socket_one.gif', 'wb')      #这是解码。保存图片
    tmp.write(base64.b64decode(socket_one))

    tmp.close()
    window = tk.Tk()
    window.title("数据挖掘演示系统")
    window.resizable(False, False)  # 固定窗口大小
    secondWidth = 800  # 获得当前窗口宽
    secondHeight = 488  # 获得当前窗口高
    screeWidth, screeHeight = window.maxsize()  # 获得屏幕宽和高
    geometryParam_second = '%dx%d+%d+%d' % (
        secondWidth, secondHeight, (screeWidth - secondWidth) / 2, (screeHeight - secondHeight) / 2)
    window.geometry(geometryParam_second)  # 设置窗口大小及偏移坐标
    window.wm_attributes('-topmost', 1)  # 窗口置顶
    #退出系统
    def exit_main():
        window.destroy()
        os.remove('socket_one.gif')
        pid = os.getpid()
        kill(pid=pid)  # 结束当前进程

    numIdx1 = 2 # gif的帧数
    photo1 = [tk.PhotoImage(file='img_bg/bg_bg.gif', format='gif -index %i' % i) for i in range(numIdx1)]

    canva= tk.Canvas(window,
                              width=800,
                              height=390,
                              bg='gray')
    im=Image.open("./img_bg/bg_main.jpg")
    img_main=ImageTk.PhotoImage(im)
    canva.create_image(400, 160, image=img_main)
    canva.pack(side=tk.BOTTOM)
    def update1(idx, ImgLabel1, love):
        frame = photo1[idx]
        idx += 1
        ImgLabel1.configure(image=frame)
        idx %= numIdx1
        love.after(200, update1, idx % numIdx1, ImgLabel1, love)

    imgLabel1 = tk.Label(window)
    imgLabel1.pack(side=tk.TOP)
    update1(0,imgLabel1,window)

    lab1=tk.Label(window,
                  text="五大常",
                  font=("楷体",25),
                  bg="#0080ff")
    lab2=tk.Label(window,
                  text='用算法',
                  font=("楷体",25),
                  bg='#0080ff')
    lab3=tk.Label(window,
                  text='---数据挖掘',
                  font=("楷体",15),
                  bg='#87CEFA'
                  )
    lab1.place(x=220,y=40)
    lab2.place(x=470,y=40)
    lab3.place(x=550,y=90)
    def c45():
        main_c45()
    def CART():
        main_CART()
    def ID3():
        main_ID3()
    def KNN():
        main_knn()
    def NAIVEBAYES():
        main_na()
    def introduct():
        root = tkinter.Tk()
        root.title('应用程序窗口')  # 窗口标题
        root.resizable(False, False)  # 固定窗口大小
        windowWidth = 800  # 获得当前窗口宽
        windowHeight = 500  # 获得当前窗口高
        screenWidth, screenHeight = root.maxsize()  # 获得屏幕宽和高
        geometryParam = '%dx%d+%d+%d' % (
            windowWidth, windowHeight, (screenWidth - windowWidth) / 2, (screenHeight - windowHeight) / 2)
        root.geometry(geometryParam)  # 设置窗口大小及偏移坐标
        root.wm_attributes('-topmost', 1)  # 窗口置顶

        scr = ScrolledText(root, width=80, height=30, font=("隶书", 15))  # 滚动文本框（宽，高（这里的高应该是以行数为单位），字体样式）
        scr.pack(side=tk.LEFT)  # 滚动文本框在页面的位置
        a = open('jianjie.txt', 'r')
        x = a.read()
        scr.insert(tk.INSERT,x)
        a.close()

        root.mainloop()
    buttton1=tk.Button(window,
                       text='五大算法简介',
                       font=('黑体',20),
                       bg='#00aeae',
                       command=introduct)
    buttton2=tk.Button(window,
                       text='    C45   ',
                       font=('黑体',20),
                       command=c45,
                       bg='#2828ff')
    buttton3=tk.Button(window,
                       text='    CART  ',
                       font=('黑体',20),
                       command=CART,
                       bg='#6a6aff')
    buttton4=tk.Button(window,
                       text='    ID3   ',
                       font=('黑体',20),
                       command=ID3,
                       bg='#005ab5')
    buttton5=tk.Button(window,
                       text='    KNN   ',
                       font=('黑体',20),
                       command=KNN,
                       bg='#0072e3')
    buttton6=tk.Button(window,
                       text='NAIVEBAYES',
                       font=('黑体',20),
                       command=NAIVEBAYES,
                       bg='#2894ff')
    buttton7=tk.Button(window,
                       text='退出系统',
                       font=('黑体',18),
                       bg='#019858',
                       command=exit_main)
    buttton1.place(x=40,y=150)
    buttton2.place(x=350,y=150)
    buttton3.place(x=350,y=210)
    buttton4.place(x=350,y=270)
    buttton5.place(x=350,y=330)
    buttton6.place(x=350,y=390)
    buttton7.place(x=650,y=420)
    window.mainloop()
if __name__ == '__main__':
    host()