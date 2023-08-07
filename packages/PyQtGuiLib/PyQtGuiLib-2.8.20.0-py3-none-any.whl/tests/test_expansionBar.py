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
)

# 测试文件

class Test_Expansionbar(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test_Expansionbar()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
