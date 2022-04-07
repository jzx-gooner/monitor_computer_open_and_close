#!/usr/bin/env python
# -*- coding: utf-8 -*-

import win32api
import win32con, winreg, os, sys
import pywintypes

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import shutil


def Judge_Key(key_name=None,
              reg_root=win32con.HKEY_CURRENT_USER,  # 根节点
              reg_path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",  # 键的路径
              abspath=None
              ):
    """
	:param key_name: #  要查询的键名
	:param reg_root: # 根节点
		#win32con.HKEY_CURRENT_USER
		#win32con.HKEY_CLASSES_ROOT
		#win32con.HKEY_CURRENT_USER
		#win32con.HKEY_LOCAL_MACHINE
		#win32con.HKEY_USERS
		#win32con.HKEY_CURRENT_CONFIG
	:param reg_path: #  键的路径
	:return:feedback是（0/1/2/3：存在/不存在/权限不足/报错）
	"""
    reg_flags = win32con.WRITE_OWNER | win32con.KEY_WOW64_64KEY | win32con.KEY_ALL_ACCESS
    try:
        key = winreg.OpenKey(reg_root, reg_path, 0, reg_flags)
        location, type = winreg.QueryValueEx(key, key_name)
        print("键存在", "location（数据）:", location, "type:", type)
        feedback = 0
        if location != abspath:
            feedback = 1
            print('键存在，但程序位置发生改变')
    except FileNotFoundError as e:
        print("键不存在", e)
        feedback = 1
    except PermissionError as e:
        print("权限不足", e)
        feedback = 2
    except:
        print("Error")
        feedback = 3
    return feedback


"""开机自启动"""


def AutoRun(switch="open",  # 开：open # 关：close
            key_name=None):
    # 如果没有自定义路径，就用os.path.abspath(sys.argv[0])获取主程序的路径，如果主程序已经打包成exe格式，就相当于获取exe文件的路径
    judge_key = Judge_Key(reg_root=win32con.HKEY_CURRENT_USER,
                          reg_path=r"Software\Microsoft\Windows\CurrentVersion\Run",  # 键的路径
                          key_name=key_name,
                          abspath=r"test\test.exe")
    # 注册表项名
    KeyName = r'Software\Microsoft\Windows\CurrentVersion\Run'
    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
    if switch == "open":
        # 异常处理
        try:
            if judge_key == 0:
                return "old exists"
            elif judge_key == 1:
                abspath=os.path.abspath(r"rtds_computer_monitor\rtds_computer_monitor.exe")
                print(abspath)
                win32api.RegSetValueEx(key, key_name, 0, win32con.REG_SZ, abspath)
                win32api.RegCloseKey(key)
                return "success ! restart computer to take effect"
        except:
            return "add failed"
    elif switch == "close":
        try:
            if judge_key == 0:
                win32api.RegDeleteValue(key, key_name)  # 删除值
                win32api.RegCloseKey(key)
                return "success uninstall"
            elif judge_key == 1:
                return "no key"
            elif judge_key == 2:
                return "no root"
            else:
                return "errors"
        except:
            return "uninstall failed"




class DialogDemo( QMainWindow ):

    def __init__(self, parent=None):
        super(DialogDemo, self).__init__(parent) 		
        self.setWindowTitle("软件助手")
        self.resize(800,600)

        self.btn = QPushButton( self)
        self.btn.setText("安装")  
        self.btn.move(350,100)
        self.btn.clicked.connect(self.showdialog)

        self.btn.setStyleSheet("QPushButton{background-color:rgb(65,113,156);color:white;font-size:30px;border-radius:10px;}")


        self.btn2 = QPushButton( self)
        self.btn2.setText("卸载")  
        self.btn2.move(350,200)		
        self.btn2.clicked.connect(self.showdialog2)
        self.btn2.setStyleSheet("QPushButton{background-color:rgb(65,113,156);color:white;font-size:30px;border-radius:10px;}")

        self.btn3 = QPushButton( self)
        self.btn3.setText("信息导出")  
        self.btn3.move(350,300)		
        self.btn3.clicked.connect(self.save_result)
        self.btn3.setStyleSheet("QPushButton{background-color:rgb(65,113,156);color:white;font-size:20px;border-radius:10px;}")

        self.btn4 = QPushButton( self)
        self.btn4.setText("信息清空")  
        self.btn4.move(350,400)		
        self.btn4.clicked.connect(self.clear_result)
        self.btn4.setStyleSheet("QPushButton{background-color:rgb(65,113,156);color:white;font-size:20px;border-radius:10px;}")

                
    def showdialog(self ):
        result = AutoRun(switch="open",key_name="rtds_computer_monitor")
        yn = QMessageBox.information(self, '信息提示对话框',result,QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
        if yn == QMessageBox.Yes:
            sys.exit(app.exec_())
    def showdialog2(self ):
        result = AutoRun(switch="close",key_name="rtds_computer_monitor")
        yn = QMessageBox.information(self, '信息提示对话框',result,QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
        if yn == QMessageBox.Yes:
            sys.exit(app.exec_())

    def save_result(self ):
        dir_choose = QFileDialog.getExistingDirectory(self,  
                                    "选取文件夹") # 起始路径

        if dir_choose == "":
            print("\n取消选择")
            return
        print("\n你选择的文件夹为:")
        print(dir_choose)
        new_dir = dir_choose + "\\" + 'statistics.csv'
        csv_path = "rtds_computer_monitor\\statistics.csv"
        shutil.copy(csv_path,new_dir)
        print("finished")
        yn = QMessageBox.information(self, '保存文件',new_dir,QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
        if yn == QMessageBox.Yes:
            sys.exit(app.exec_())
        # sys.exit(app.exec_())
    def clear_result(self):
        yn = QMessageBox.information(self, '清空信息','是否确认清空登记信息',QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
        if yn == QMessageBox.Yes:
            csv_path = r"rtds_computer_monitor\statistics.csv"
            with open(csv_path, 'w') as csv_file:
                csv_file.write("姓名"+","+"学号"+","+"导师"+","+"上机时间"+","+"下机时间"+ ","+"登陆时长" +"\n")
        yn = QMessageBox.information(self, '清空信息','完成清理',QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
        if yn == QMessageBox.Yes:
            sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = DialogDemo()
    demo.show()
    sys.exit(app.exec_())