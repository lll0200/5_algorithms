# -*- codeing = utf-8 -*-
# @Time :2021/5/18 20:50
# @Author : 刘念卿
# @File : CART.py
# @Software : PyCharm
import tkinter as tk
from tkinter.filedialog import askdirectory
import pandas as pd
import time
from tkinter.messagebox import showerror
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from PIL import Image, ImageTk
from sklearn.tree import DecisionTreeClassifier
# 选择文件路径
def select_file():
    global entry
    def selectPath():
        # 选择文件path_接收文件地址
        path_ = tk.filedialog.askopenfilename()
        # 通过replace函数替换绝对文件地址中的/来使文件可被程序读取
        # 注意：\\转义后为\，所以\\\\转义后为\\
        path_ = path_.replace("/", "\\")
        entry.insert(0,path_)
    Label = tk.Label(window, text="文件路径:", font=('黑体', 12))
    Label.place(x=20, y=20)
    entry = tk.Entry(window)
    entry.place(x=100, y=20)
    button = tk.Button(window, text="check", command=selectPath, font=('黑体', 12))
    button.place(x=260, y=16)

def ok():
    def _main():
        path = entry.get()

        b = "Start read data...\n"

        time_1 = time.time()
        try:
            raw_data = pd.read_csv(path, header=0)
            data = raw_data.values
            text0.insert(tk.INSERT, b)

            features = data[::, 1::]
            labels = data[::, 0]

            # 随机选取33%数据作为测试集，剩余为训练集
            train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.33,
                                                                                        random_state=0)

            time_2 = time.time()
            c = ('read data cost %f seconds\n' % (time_2 - time_1))
            text0.insert(tk.INSERT, c)

            d = 'Start training...\n'
            text0.insert(tk.INSERT, d)
            # criterion可选‘gini’, ‘entropy’，默认为gini(对应CART算法)，entropy为信息增益（对应ID3算法）
            clf = DecisionTreeClassifier(criterion='gini')
            clf.fit(train_features, train_labels)
            time_3 = time.time()
            e = ('training cost %f seconds\n' % (time_3 - time_2))
            text0.insert(tk.INSERT, e)

            f = 'Start predicting...\n'
            text0.insert(tk.INSERT, f)
            test_predict = clf.predict(test_features)
            time_4 = time.time()
            g = ('predicting cost %f seconds\n' % (time_4 - time_3))
            text0.insert(tk.INSERT, g)

            score = accuracy_score(test_labels, test_predict)
            s = ("The accruacy score is %f" % score)
            text0.insert(tk.INSERT, s)
        except FileNotFoundError :
            tk.messagebox.showerror('错误', '文件错误或不存在！')
    button = tk.Button(window,
                           text='ok',
                           command=_main,
                           font=('黑体', 15)
                           )
    button.place(x=180, y=180)
    def e():
        window.destroy()
    button1 = tk.Button(window,
                       text='退出',
                       command=e,
                       font=('黑体', 15)
                       )
    button1.place(x=320, y=190)
    global text0
    text0 = tk.Text(window,
                    width=40,
                    height=8)
    text0.place(x=80, y=50)
    lab = tk.Label(window,
                   text="结\n果",
                   font=("黑体", 20))
    lab.place(x=25, y=80)
def main_CART():
    global window
    window = tk.Tk()
    window.title("CART")
    window.resizable(False, False)  # 固定窗口大小
    secondWidth = 400  # 获得当前窗口宽
    secondHeight = 245  # 获得当前窗口高
    screeWidth, screeHeight = window.maxsize()  # 获得屏幕宽和高
    geometryParam_second = '%dx%d+%d+%d' % (
        secondWidth, secondHeight, (screeWidth - secondWidth) / 2, (screeHeight - secondHeight) / 2)
    window.geometry(geometryParam_second)  # 设置窗口大小及偏移坐标
    window.wm_attributes('-topmost', 1)  # 窗口置顶
    canvas = tk.Canvas(window,
                       width=400,  # 指定Canvas组件的宽度
                       height=245,  # 指定Canvas组件的高度
                       bg='#00B3A1')  # 指定Canvas组件的背景色
    # image = Image.open("bg_2.jpg")
    # im = ImageTk.PhotoImage(image)
    # canvas.create_image(300, 50, image=im)
    canvas.pack(side=tk.LEFT)
    select_file()
    ok()
    window.mainloop()

# if __name__ == '__main__':
#     main_CART()