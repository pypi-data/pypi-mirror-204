# -*- coding:utf-8 -*-
# @time:2023-04-17 14:35
# @author:LX
# @file:expansionBar.py
# @software:PyCharm

from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QPushButton,
    QIcon,
    QSpacerItem,
    QSizePolicy,
    QPropertyAnimation,
    QSize,
    QObject
)

from PyQtGuiLib.styles import QssStyleAnalysis

'''
    伸缩栏
'''

class ExpansionBar(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(210,550)
        self.setObjectName("widget")

        self.__items = []

        self.__core_vboy = QVBoxLayout(self)
        # self.__core_vboy.setContentsMargins(3,3,3,3)
        self.addHeader()
        self.__body_form = QFormLayout()
        self.__core_vboy.addLayout(self.__body_form)
        self.__body_form.setHorizontalSpacing(0)

        self.addItem("hello","")
        self.addItem("hello","")
        self.addItem("hello","")
        # self.__core_vboy.addItem(self.__ver_sitem)

        self.__qss = QssStyleAnalysis(self)

        self.myEvent()
        self.defaultStyle()

    def addHeader(self):
        self.__btn_head = QPushButton("三")
        self.__btn_head.setObjectName("head_btn")
        self.__btn_head.setFixedSize(50, 50)

        hboy = QHBoxLayout()
        hboy.addWidget(self.__btn_head)


        self.__core_vboy.addLayout(hboy)

    def addItem(self,text:str,icon:str):
        label = QLabel()
        btn = QPushButton()
        label.setFixedSize(50,50)
        btn.setFixedHeight(50)

        # label.setWindowIcon(QIcon(r"D:\code\PyQtGuiLib\tests\temp_image\python1.png"))
        btn.setText("Hello")

        self.__body_form.addRow(label,btn)

        self.__items.append((label,btn))


    def defaultStyle(self):
        self.__qss.setQSS('''
#widget{
	/*background-color: rgba(27, 27, 27, 200);*/
	border-radius:5px;
}
QLabel{
background-color: qlineargradient(spread:pad, x1:0, y1:0.574136, x2:0.984, y2:0.58, stop:0 rgba(118, 176, 189, 255), stop:1 rgba(0, 0, 0, 255));
color: rgb(255, 255, 255);
border-top-left-radius:25px;
border-bottom-left-radius:25px;
}
QPushButton{
background-color: qlineargradient(spread:pad, x1:0, y1:0.551136, x2:1, y2:0.545455, stop:0 rgba(0, 0, 0, 255), stop:0.965909 rgba(0, 0, 0, 255));
color: rgb(255, 255, 255);
border-top-right-radius:25px;
border-bottom-right-radius:25px;
}
#head_btn{
background-color: rgb(0, 0, 0);
color: rgb(255, 255, 255);
border-radius:25px;
}
''')
        self.__qss.selector("QLabel").updateAttr("border-top-right-radius","0px")
        self.__qss.selector("QLabel").updateAttr("border-bottom-right-radius","0px")

    def __t(self,v:QSize):
        for la,btn in self.__items:
            btn:QPushButton
            btn.setFixedWidth(v.width())

    def __t2(self,v:QSize):
        self.__qss.selector("QLabel").updateAttr("border-top-right-radius","{}px".format(v.width()))
        self.__qss.selector("QLabel").updateAttr("border-bottom-right-radius","{}px".format(v.width()))

    def __ani_event(self):
        self.ani = QPropertyAnimation(self,b"size")
        self.ani.setDuration(400)
        self.ani.setStartValue(self.size())
        self.ani.setEndValue(QSize(50,self.height()))
        self.ani.valueChanged.connect(self.__t)
        self.ani.start()

        self.ani2 = QPropertyAnimation(QLabel(),b"size")
        self.ani2.setDuration(400)
        self.ani2.setStartValue(QSize(0,100))
        self.ani2.setEndValue(QSize(25, 100))
        self.ani2.valueChanged.connect(self.__t2)
        self.ani2.start()


        def _hide():
            for la,btn in self.__items:
                btn.hide()

        self.ani2.finished.connect(_hide)


    def myEvent(self):
        self.__btn_head.clicked.connect(self.__ani_event)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = ExpansionBar()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
