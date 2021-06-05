# -*- codeing = utf-8 -*-
# @Time :2021/5/19 10:25
# @Author : 刘念卿
# @File : not_gif.py
# @Software : PyCharm
# -*- coding: utf-8 -*-


import base64

def pic2py(picture_name):     #把图片用base64编码保存在文件里面。
    """
    将图像文件转换为py文件
    :param picture_name:
    :return:
    """
    open_pic = open("%s" % picture_name, 'rb')  #python 内置函数open()  用于打开一个文件
                                                #rb 以二进制格式打开一个文件用于只读。文件指针将会放在文件的开头。这是默认模式
    b64str = base64.b64encode(open_pic.read())
    # 注意这边b64str一定要加上.decode()
    write_data = 'img = "%s"' % b64str.decode()
    f = open('%s.py' % picture_name.replace('.', '_'), 'w+')  #打开一个文件用于读写。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。
    f.write(write_data)
    f.close()

    """
    通俗的理解__name__ == '__main__'：假如你叫小明.py，在朋友眼中，你是小明(__name__ == '小明')；在你自己眼中，你是你自己(__name__ == '__main__')。
    if __name__ == '__main__'的意思是：当.py文件被直接运行时，if __name__ == '__main__'之下的代码块将被运行；当.py文件以模块形式被导入时，if __name__ == '__main__'之下的代码块不被运行。
    """

if __name__ == '__main__':
    pics = ["bg_bg.gif"]     #//这个文件我们只需要改这里的这个list变量，它的元素就是我们要使用的图片的全名加后缀
    for i in pics:
        pic2py(i)
    print("ok")