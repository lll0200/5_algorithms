# -*- codeing = utf-8 -*-
# @Time :2021/5/18 10:21
# @Author : 刘念卿
# @File : knn.py
# @Software : PyCharm
from numpy import *
import operator

#定义KNN算法分类器函数
#函数参数包括：(测试数据，训练数据，分类,k值)
def classify(inX,dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX,(dataSetSize,1))-dataSet
    sqDiffMat=diffMat**2
    sqDistances=sqDiffMat.sum(axis=1)
    distances=sqDistances**0.5 #计算欧式距离
    sortedDistIndicies=distances.argsort() #排序并返回index
    #选择距离最近的k个值
    classCount={}
    for i in range(k):
        voteIlabel=labels[sortedDistIndicies[i]]
        #D.get(k[,d]) -> D[k] if k in D, else d. d defaults to None.
        classCount[voteIlabel]=classCount.get(voteIlabel,0)+1
    #排序
    sortedClassCount=sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]