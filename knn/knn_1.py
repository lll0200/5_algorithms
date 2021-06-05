# -*- codeing = utf-8 -*-
# @Time :2021/5/18 10:21
# @Author : 刘念卿
# @File : knn_1.py
# @Software : PyCharm
import tkinter as tk
import tkinter.messagebox
import numpy as np
from PIL import Image, ImageTk
from numpy import *
import operator
def main_knn():
    global windows
    windows=tk.Tk()
    windows.title("KNN算法")
    windows.resizable(False, False)  # 固定窗口大小
    windowWidth = 400  # 获得当前窗口宽
    windowHeight = 245  # 获得当前窗口高
    screenWidth, screenHeight = windows.maxsize()  # 获得屏幕宽和高
    geometryParam = '%dx%d+%d+%d' % (
        windowWidth, windowHeight, (screenWidth - windowWidth) / 2, (screenHeight - windowHeight) / 2)
    windows.geometry(geometryParam)  # 设置窗口大小及偏移坐标
    windows.wm_attributes('-topmost', 1)  # 窗口置顶
    canvas = tk.Canvas(windows,
                       width=400,  # 指定Canvas组件的宽度
                       height=245,  # 指定Canvas组件的高度
                       bg='#00B300')  # 指定Canvas组件的背景色
    # image = Image.open("bg_4.jpg")
    # im = ImageTk.PhotoImage(image)
    # canvas.create_image(300, 50, image=im)
    canvas.pack(side=tk.LEFT)
    global button1, button2

    button1=tk.Button(windows,
                      text="示例1",
                      font=("楷体",15),
                      command=Examples_1
                      )
    button2 = tk.Button(windows,
                        text="示例2",
                        font=("楷体", 15),
                        command=Examples_2
                        )

    a=125
    button1.place(x=a,y=55)
    button2.place(x=a,y=135)
    button5 = tk.Button(windows,
                        text="退出",
                        font=("楷体", 15),
                        command=return_main
                        )
    button5.place(x=335,y=205)
    windows.mainloop()
#按钮
def button_c(a):
    global entyr ,lable,lable1,button
    entyr = tk.Entry(windows)
    entyr.place(x=135, y=118)
    lable = tk.Label(windows,
                     text="请输入k值：",
                     font=('黑体', 15))
    lable.place(x=15, y=115)
    lable1 = tk.Label(windows,
                      text="所属类别： ",
                      font=('黑体', 15))
    lable1.place(x=15, y=145)
    button = tk.Button(windows,
                       text="ok",
                       font=("黑体", 15),
                       command=a)
    button.place(x=175, y=195)
#隐藏按钮
def hide_button():
    button1.place_forget()
    button2.place_forget()
#示例1
def Examples_1():
    text=tk.Text(windows,
                 width=10,
                 height=1.45)
    text.place(x=150,y=148)
    lab=tk.Label(windows,
                 text='训练样本：[[1, 1.1], [1, 1], [0, 0], [0, 0.1]]',
                 font=('楷体',12)
                 )
    lab.place(x=5,y=10)
    lab1 = tk.Label(windows,
                   text='对应标签：A, A, B, B',
                   font=('楷体', 12)
                   )
    lab1.place(x=5, y=30)
    lab2 = tk.Label(windows,
                   text='测试数据：[0,0]',
                   font=('楷体', 12)
                   )
    lab2.place(x=5, y=50)
    def a():
        windows.destroy()
        main_knn()
    button5 = tk.Button(windows,
                        text="返回",
                        font=("楷体", 15),
                        command=a
                        )
    button5.place(x=335,y=205)
    def ok():
        if entyr.get().isdigit():
            K=int(entyr.get())
            # print(type(K))
            def createDataSet():
                Group=np.array([[1, 1.1], [1, 1], [0, 0], [0, 0.1]])
                Labels=['A', 'A', 'B', 'B']
                return Group, Labels

            def classify(inX, dataSet, Labels, kk):
                dataSetSize = dataSet.shape[0]
                diffMat = tile(inX, (dataSetSize, 1)) - dataSet
                sqDiffMat = diffMat ** 2
                sqDistances = sqDiffMat.sum(axis=1)
                distances = sqDistances ** 0.5  # 计算欧式距离
                sortedDistIndicies = distances.argsort()  # 排序并返回index
                # 选择距离最近的k个值
                classCount = {}
                for i in range(kk):
                    voteIlabel = Labels[sortedDistIndicies[i]]
                    # D.get(k[,d]) -> D[k] if k in D, else d. d defaults to None.
                    classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
                # 排序
                sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
                return sortedClassCount[0][0]

            #生成训练样本
            group,labels=createDataSet()
            #对测试数据[0,0]进行KNN算法分类测试
            result=classify([0,0], group, labels, K)
            text.delete(0.0,'end')
            text.insert(tk.INSERT,result)
            #print('category:',result)
        else:
            tk.messagebox.showwarning('警告', '请输入数字！')
    hide_button()
    button_c(ok)
    #定义一个生成“训练样本集”的函数，包含特征和分类信息

#示例2
def Examples_2():
    hide_button()
    text=tk.Text(windows,
                 width=10,
                 height=1.45)
    text.place(x=135,y=148)
    E = tkinter.Variable()
    entry2 = tkinter.Entry(windows, textvariable=E)
    entry2.place(x=130,y=85)
    E.set("唐人街探案")  # 设置默认值 :23,3,17
    lable=tk.Label(windows,
                   text="请输入名：",
                   font=('黑体',15))
    lable.place(x=15,y=85)
    lab=tk.Label(windows,
                 text="例子：\n名称:唐人街探案\n搞笑:23\n拥抱:3\n打斗:17",
                 anchor='center')
    lab.place(x=290,y=75)
    E1 = tkinter.Variable()

    entry2 = tkinter.Entry(windows,textvariable=E1)
    entry2.place(x=160, y=5)
    lable1 = tk.Label(windows,
                     text="搞笑镜头数量：",
                     font=('黑体', 12))
    lable1.place(x=15, y=5)
    E1.set("23")

    E2 = tkinter.Variable()
    entry3 = tkinter.Entry(windows,textvariable=E2)
    entry3.place(x=160, y=30)
    E2.set("3")
    lable2 = tk.Label(windows,
                      text="拥抱镜头数量：",
                      font=('黑体', 12))
    lable2.place(x=15, y=30)

    E3 = tkinter.Variable()
    entry4 = tkinter.Entry(windows,textvariable=E3)
    entry4.place(x=160, y=55)
    E3.set("17")
    lable3 = tk.Label(windows,
                      text="打斗镜头数量：",
                      font=('黑体', 12))
    lable3.place(x=15, y=55)
    def a():
        windows.destroy()
        main_knn()
    button5 = tk.Button(windows,
                        text="返回",
                        font=("楷体", 15),
                        command=a
                        )
    button5.place(x=335,y=205)
    def two():
        def createDataset():
            '''
            创建训练集,特征值分别为搞笑镜头、拥抱镜头、打斗镜头的数量
            '''
            learning_dataset = {"宝贝当家": [45, 2, 9, "喜剧片"],
                                "美人鱼": [21, 17, 5, "喜剧片"],
                                "澳门风云3": [54, 9, 11, "喜剧片"],
                                "功夫熊猫3": [39, 0, 31, "喜剧片"],
                                "谍影重重": [5, 2, 57, "动作片"],
                                "叶问3": [3, 2, 65, "动作片"],
                                "伦敦陷落": [2, 3, 55, "动作片"],
                                "我的特工爷爷": [6, 4, 21, "动作片"],
                                "奔爱": [7, 46, 4, "爱情片"],
                                "夜孔雀": [9, 39, 8, "爱情片"],
                                "代理情人": [9, 38, 2, "爱情片"],
                                "新步步惊心": [8, 34, 17, "爱情片"]}
            return learning_dataset

        def kNN(learning_dataset, dataPoint, k):
            '''
            kNN算法,返回k个邻居的类别和得到的测试数据的类别
            '''
            # s1:计算一个新样本与数据集中所有数据的距离
            disList = []
            for key, v in learning_dataset.items():
                d = np.linalg.norm(np.array(v[:3]) - np.array(dataPoint))
                disList.append([key, round(d, 2)])

            # s2:按照距离大小进行递增排序
            disList.sort(key=lambda dis: dis[1])

            # s3:选取距离最小的k个样本
            disList = disList[:k]

            # s4:确定前k个样本所在类别出现的频率，并输出出现频率最高的类别
            labels = {"喜剧片": 0, "动作片": 0, "爱情片": 0}
            for s in disList:
                label = learning_dataset[s[0]]
                labels[label[len(label) - 1]] += 1
            labels = sorted(labels.items(), key=lambda asd: asd[1], reverse=True)

            return labels, labels[0][0]

        learning_dataset = createDataset()

        #testData = {"唐人街探案": [23, 3, 17, "？片"]}
        #dataPoint = list(testData.values())[0][:3]
        dataPoint=[]
        if entyr.get().isdigit() and entry2.get().isdigit() and entry3.get().isdigit() and entry4.get().isdigit():
            k1 = int(entyr.get())
            dataPoint.append(int(entry2.get()))
            dataPoint.append(int(entry3.get()))
            dataPoint.append(int(entry4.get()))
            labels, result = kNN(learning_dataset, dataPoint, k1)
            #print(labels, result, sep='\n')
            text.insert(tk.INSERT,result)
        else:
            tk.messagebox.showwarning('警告', '请输入数字！')
    button_c(two)

def return_main():
    windows.destroy()
# if __name__ == '__main__':
#     main_knn()