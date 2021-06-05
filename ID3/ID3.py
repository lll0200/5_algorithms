# -*- codeing = utf-8 -*-
# @Time :2021/5/18 15:48
# @Author : 刘念卿
# @File : C45.py
# @Software : PyCharm
import tkinter as tk
from tkinter.filedialog import askdirectory
import cv2
import time
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from tkinter.messagebox import showerror
from PIL import Image, ImageTk

# 选择文件路径
def select_file():
    global entry
    def selectPath():
        # 选择文件path_接收文件地址
        path_ = tk.filedialog.askopenfilename()
        # 通过replace函数替换绝对文件地址中的/来使文件可被程序读取
        # 注意：\\转义后为\，所以\\\\转义后为\\
        path_ = path_.replace("/", "\\")
        # path设置path_的值
        entry.insert(0,path_)

    Label = tk.Label(window, text="文件路径:", font=('黑体', 12))
    Label.place(x=20, y=20)
    entry = tk.Entry(window)
    entry.place(x=100, y=20)
    button = tk.Button(window, text="check", command=selectPath, font=('黑体', 12))
    button.place(x=260, y=16)

def ok():
    # 二值化
    def binaryzation(img):
        cv_img = img.astype(np.uint8)
        cv2.threshold(cv_img, 50, 1, cv2.THRESH_BINARY_INV, cv_img)
        return cv_img

    def binaryzation_features(trainset):
        features = []

        for img in trainset:
            img = np.reshape(img, (28, 28))
            cv_img = img.astype(np.uint8)

            img_b = binaryzation(cv_img)
            # hog_feature = np.transpose(hog_feature)
            features.append(img_b)

        features = np.array(features)
        features = np.reshape(features, (-1, feature_len))

        return features

    class Tree(object):
        def __init__(self, node_type, Class=None, feature=None):
            self.node_type = node_type  # 节点类型（internal或leaf）
            self.dict = {}  # dict的键表示特征Ag的可能值ai，值表示根据ai得到的子树
            self.Class = Class  # 叶节点表示的类，若是内部节点则为none
            self.feature = feature  # 表示当前的树即将由第feature个特征划分（即第feature特征是使得当前树中信息增益最大的特征）

        def add_tree(self, key, tree):
            self.dict[key] = tree

        def predict(self, features):
            if self.node_type == 'leaf' or (features[self.feature] not in self.dict):
                return self.Class

            tree = self.dict.get(features[self.feature])
            return tree.predict(features)

    # 计算数据集x的经验熵H(x)
    def calc_ent(x):
        x_value_list = set([x[i] for i in range(x.shape[0])])
        ent = 0.0
        for x_value in x_value_list:
            p = float(x[x == x_value].shape[0]) / x.shape[0]
            logp = np.log2(p)
            ent -= p * logp

        return ent

    # 计算条件熵H(y/x)
    def calc_condition_ent(x, y):
        x_value_list = set([x[i] for i in range(x.shape[0])])
        ent = 0.0
        for x_value in x_value_list:
            sub_y = y[x == x_value]
            temp_ent = calc_ent(sub_y)
            ent += (float(sub_y.shape[0]) / y.shape[0]) * temp_ent

        return ent

    # 计算信息增益
    def calc_ent_grap(x, y):
        base_ent = calc_ent(y)
        condition_ent = calc_condition_ent(x, y)
        ent_grap = base_ent - condition_ent

        return ent_grap

    # ID3算法
    def recurse_train(train_set, train_label, features):

        LEAF = 'leaf'
        INTERNAL = 'internal'

        # 步骤1——如果训练集train_set中的所有实例都属于同一类Ck
        label_set = set(train_label)
        if len(label_set) == 1:
            return Tree(LEAF, Class=label_set.pop())

        # 步骤2——如果特征集features为空
        class_len = [(i, len(list(filter(lambda x: x == i, train_label)))) for i in range(class_num)]  # 计算每一个类出现的个数
        (max_class, max_len) = max(class_len, key=lambda x: x[1])

        if len(features) == 0:
            return Tree(LEAF, Class=max_class)

        # 步骤3——计算信息增益,并选择信息增益最大的特征
        max_feature = 0
        max_gda = 0
        D = train_label
        for feature in features:
            # print(type(train_set))
            A = np.array(train_set[:, feature].flat)  # 选择训练集中的第feature列（即第feature个特征）
            gda = calc_ent_grap(A, D)
            if gda > max_gda:
                max_gda, max_feature = gda, feature

        # 步骤4——信息增益小于阈值
        if max_gda < epsilon:
            return Tree(LEAF, Class=max_class)

        # 步骤5——构建非空子集
        sub_features = list(filter(lambda x: x != max_feature, features))
        tree = Tree(INTERNAL, feature=max_feature)

        max_feature_col = np.array(train_set[:, max_feature].flat)
        feature_value_list = set(
            [max_feature_col[i] for i in range(max_feature_col.shape[0])])  # 保存信息增益最大的特征可能的取值 (shape[0]表示计算行数)
        for feature_value in feature_value_list:

            index = []
            for i in range(len(train_label)):
                if train_set[i][max_feature] == feature_value:
                    index.append(i)

            sub_train_set = train_set[index]
            sub_train_label = train_label[index]

            sub_tree = recurse_train(sub_train_set, sub_train_label, sub_features)
            tree.add_tree(feature_value, sub_tree)

        return tree

    def train(train_set, train_label, features):
        return recurse_train(train_set, train_label, features)

    def predict(test_set, tree):
        result = []
        for features in test_set:
            tmp_predict = tree.predict(features)
            result.append(tmp_predict)
        return np.array(result)

    class_num = 10  # MINST数据集有10种labels，分别是“0,1,2,3,4,5,6,7,8,9”
    feature_len = 784  # MINST数据集每个image有28*28=784个特征（pixels）
    epsilon = 0.001  # 设定阈值



    def _main():
        path=entry.get()
        try:
            b = "Start read data...\n"


            time_1 = time.time()

            raw_data = pd.read_csv(path, header=0)  # 读取csv数据
            data = raw_data.values
            text0.insert(tk.INSERT, b)
            imgs = data[::, 1::]
            features = binaryzation_features(imgs)  # 图片二值化(很重要，不然预测准确率很低)
            labels = data[::, 0]

            # 避免过拟合，采用交叉验证，随机选取33%数据作为测试集，剩余为训练集
            train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.33,
                                                                                        random_state=0)
            time_2 = time.time()
            c = ('read data cost %f seconds\n' % (time_2 - time_1))
            text0.insert(tk.INSERT, c)

            # 通过ID3算法生成决策树
            d = 'Start training...\n'
            text0.insert(tk.INSERT, d)
            tree = train(train_features, train_labels, list(range(feature_len)))
            time_3 = time.time()
            e = ('training cost %f seconds\n' % (time_3 - time_2))
            text0.insert(tk.INSERT, e)

            f = 'Start predicting...\n'
            text0.insert(tk.INSERT, f)
            test_predict = predict(test_features, tree)
            time_4 = time.time()
            g = ('predicting cost %f seconds\n' % (time_4 - time_3))
            text0.insert(tk.INSERT, g)
            # print("预测的结果为：")
            # print(test_predict)
            for i in range(len(test_predict)):
                if test_predict[i] is None:
                    test_predict[i] = epsilon
            score = accuracy_score(test_labels, test_predict)
            s = ("The accruacy score is %f" % score)
            text0.insert(tk.INSERT, s)

        except FileNotFoundError:
                tk.messagebox.showerror('错误', '文件错误或不存在！')

    button = tk.Button(window,
                       text='ok',
                       command=_main,
                       font=('黑体', 15)
                       )
    button.place(x=200, y=180)
    def re():
        window.destroy()
    button1 = tk.Button(window,
                        text='关闭',
                        command=re,
                        font=('黑体', 13)
                        )
    button1.place(x=120, y=200)
    lab1 = tk.Label(window,
                    text="温馨提示！\nID3算法较慢\n请耐心等待!",
                    bg="yellow")
    lab1.place(x=20, y=160)
    lab2 = tk.Label(window,
                    text="温馨提示！\n需要几分钟的时间\n请耐心等待!",
                    bg="yellow")
    lab2.place(x=280, y=160)
    global text0
    text0 = tk.Text(window,
                    width=40,
                    height=8)
    text0.place(x=80, y=50)
    lab = tk.Label(window,
                   text="结\n果",
                   font=("黑体", 20))
    lab.place(x=25, y=80)
def main_ID3():
    global window
    window = tk.Tk()
    window.title("ID3")
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
                       bg='#00B33c')  # 指定Canvas组件的背景色
    # image = Image.open("bg_3.jpg")
    # im = ImageTk.PhotoImage(image)
    # canvas.create_image(300, 50, image=im)
    canvas.pack(side=tk.LEFT)
    select_file()
    ok()
    window.mainloop()


# if __name__ == '__main__':
#     main_ID3()