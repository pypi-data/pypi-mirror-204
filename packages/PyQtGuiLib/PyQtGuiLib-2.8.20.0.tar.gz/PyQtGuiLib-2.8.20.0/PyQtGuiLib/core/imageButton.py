# -*- coding:utf-8 -*-
# @time:2023-04-17 11:53
# @author:LX
# @file:imageButton.py
# @software:PyCharm

from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QPoint,
    QPainter,
    QColor,
    QRect,
    QSize,
    QFont,
    QPen,
    QBrush,
    QPaintEvent,
    Qt,
    qt,
    QPixmap,
    QImage,
    textSize
)



class ImageButton(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.__margin = 3
        self.__radius = 5
        self.__imagePath = ""
        self.__imageSize = QSize(50,50)

    def imagePath(self)->str:
        return self.__imagePath

    def margin(self)->int:
        return self.__margin

    def radius(self)->int:
        return self.__radius

    def imageSize(self)->QSize:
        return self.__imageSize

    def paintEvent(self, e:QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)

        # 绘制矩形
        op = QPen()
        op.setWidth(2)
        op.setColor(QColor("green"))

        painter.setPen(op)
        painter.drawRoundedRect(self.margin(),self.margin(),
                                self.width()-self.margin()*2,self.height()-self.margin()*2,
                                self.radius(),self.radius())

        # 绘制文字
        f = QFont("hello")
        f.setPointSize(20)
        painter.setFont(f)

        font_size = textSize(f,"hello")
        fw = font_size.width()
        fh = font_size.height()
        fx = self.width()//2-fw//2+self.margin()*2
        fy = self.height()//2+fh//2-self.margin()

        painter.drawText(fx,
                         fy,"hello")

        # 绘制图片
        print(fy,fh)
        ix = fx - self.imageSize().width()
        if self.imageSize().height()-fh >=8:
            iy = self.height()//2-fh
            irect = QRect(QPoint(ix,iy),self.imageSize())
        else:
            iy = self.height() // 2 - 8
            irect = QRect(QPoint(ix, iy), self.imageSize())

        # painter.drawRect(irect)
        painter.drawImage(irect, QImage(r"D:\code\PyQtGuiLib\tests\temp_image\python1.png"))

        painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = ImageButton()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
