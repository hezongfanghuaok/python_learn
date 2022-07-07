import untitled
from PyQt5.QtWidgets import QApplication, QDialog,QMainWindow
import sys




class MainDialog(QDialog):

    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.ui=untitled.Ui_Form()
        self.ui.setupUi(self)

    def my_fist_button_test(self):
        print("hellow")
        self.ui.mytest_textedit.setText("fuck  aaa")


myapp = QApplication(sys.argv)

myDlg = MainDialog()

myDlg.show()

sys.exit(myapp.exec_())

if __name__ == "__main__":

    mainwindow.show()
    sys.exit(app.exec_())
    # 获取uic窗口操作权限
    app = QApplication(sys.argv)
    mainwindow = QMainWindow()
    # 调用自定义的界面（即刚刚转换的py对象）
    ui = untitled.Ui_Form()

    ui.setupUi(mainwindow)
    # 显示窗口，并释放资源
