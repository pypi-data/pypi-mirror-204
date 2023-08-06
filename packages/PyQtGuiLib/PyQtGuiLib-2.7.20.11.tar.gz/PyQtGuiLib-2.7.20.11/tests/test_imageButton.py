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
    qt
)

# 测试文件
from PyQtGuiLib.core.imageButton import ImageButton

class Test_Imagebutton(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.ibtn = ImageButton(self)
        self.ibtn.resize(150,60)
        self.ibtn.move(30,30)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test_Imagebutton()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
