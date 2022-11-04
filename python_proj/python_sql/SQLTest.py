from PyQt5.QtCore import QStringListModel

from config_sql_item import sql_executor
from PyQt5.QtWidgets import QApplication, QMainWindow
import name
import sys
from functools import partial

class Window(QMainWindow,name.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.list1=[]
        self.setupUi(self)
        self.select.clicked.connect(partial(self.sql_select_first))#partial 可传参
        self.select_M.clicked.connect(self.sql_select_multiple)
        self.update.clicked.connect(partial(self.sql_update))
        self.insert.clicked.connect(partial(self.sql_insert))
        self.model = QStringListModel()
    #选择第一行
    def sql_select_first(self):
        row=sql_executor.fetch_one("select * from sqlTest ")
        for i in row:
            self.list1.append(i)
        self.model.setStringList(self.list1)
        #self.AddItem()
        self.listView.setModel(self.model)
    def sql_select_multiple(self):
        row=sql_executor.fetch_all("select * from sqlTest ")
        for i in row:
            for c in i:
                self.list1.append(c)
        self.model.setStringList(self.list1)
        #self.AddItem()
        self.listView.setModel(self.model)
    def sql_insert(self):
        sql_executor.execute("insert into sqlTest (id,name) values ('3','l')")
        self.list1.append("insert zhixingyici")
        self.model.setStringList(self.list1)
        self.listView.setModel(self.model)
    def sql_update(self):
        sql_executor.execute("update sqltest set id ='10'")
        self.list1.append("update zhixingyici")
        self.model.setStringList(self.list1)
        self.listView.setModel(self.model)
'''
    def AddItem(self):
        count = self.model.rowCount()
        selectindex = self.listView.currentIndex()
        if selectindex.isValid():
            Pos = selectindex.row()  # 取当前选择的数据项位置的顺序索引
        else:
            Pos = count  # 当前没有选择则插入到最后位置
        self.model.insertRow(Pos)  # 执行插入位置元素扩充
        index = self.model.index(Pos, 0)  # 取插入位置的元素项
        stritem = f'item{Pos + 1}'  # 设置插入内容
        self.model.setData(index, stritem)  # 将内容更新到插入位置
'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()

    window.show()

    sys.exit(app.exec_())
