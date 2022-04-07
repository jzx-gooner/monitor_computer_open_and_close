#coding=utf-8
import sys
import os
import time  
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import datetime


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def read_info_and_add_to_csv():
    log_path=resource_path("log.txt")
    csv_path=resource_path("statistics.csv")
    if log_path:
        with open(log_path, 'r+') as log_file:
            lines = log_file.readlines()
            if len(lines) < 2:
                return
            else:
                # if len(lines) == 1:
                #     first_line = lines[0]
                #     print(first_line)
                #     name,xuehao,daoshi,start_time= first_line.strip().split(",")
                #     end_time = start_time
                #     duration_time= "不足1min"
                # else:
                first_line = lines[0]
                last_line = lines[-1]
                if not last_line.startswith("run"):
                    return
                name,xuehao,daoshi,start_time= first_line.strip().split(",")
                end_time = last_line.strip().split(",")[-1]
                time_diff = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                minutes = int(time_diff.total_seconds()/60)
                duration_time = str(minutes//60) + 'h' + str(minutes%60).rjust(2,'0')+"m"
                #清空内容
                print("清空内容")
                log_file.truncate(0)
        with open(csv_path, 'a') as csv_file:
            csv_file.write(name+","+xuehao+","+daoshi+","+start_time+","+end_time+ ","+duration_time +"\n")
            
class LoginForm(QWidget):
  def __init__(self):
    super().__init__()
    self.initUI()
  def initUI(self):
    """
    初始化UI
    :return:
    """
    icon_path = resource_path("logo.jpg")

    self.setObjectName("loginWindow")
    self.setStyleSheet('#loginWindow{background-color:white}')

    global width,height
    self.width = width
    self.height = height
    self.setFixedSize(self.width, self.height)
    self.setWindowTitle("RTDS_COMPUTER_MONITOR")
    self.setWindowIcon(QIcon(icon_path))
    self.setWindowFlags(Qt.WindowCloseButtonHint ) #| Qt.WindowType_Mask #隐藏关闭按钮
    self.setWindowFlags(Qt.WindowStaysOnTopHint) #始终处于顶层显示
    self.setWindowFlags(Qt.FramelessWindowHint) #隐藏任务栏图标 #Qt.SplashScreen | 
    # self.setWindowFlags(Qt.ToolTip)
  
    self.text = "欢迎使用RTDS实时数字仿真系统！"+"\n"+"请录入使用者信息:"
  
    # 添加顶部logo图片
    pixmap = QPixmap(icon_path)
    # scaredPixmap = pixmap.scaled(672, 674)
    scaredPixmap = pixmap.scaled(516, 518)
    label = QLabel(self)
    label.setPixmap(scaredPixmap)
    label.move(int(self.width*0.7), int(self.height*0.5))
  
    # 绘制顶部文字
    lbl_logo = QLabel(self)
    lbl_logo.setText(self.text)
    lbl_logo.setStyleSheet("QWidget{color:rgb(65, 113, 156);font-weight:700;background: transparent;font-size:50px;}")
    lbl_logo.setFont(QFont("Microsoft YaHei"))
    lbl_logo.move(self.width/2 *0.65, 140)
    lbl_logo.setAlignment(Qt.AlignCenter)
    lbl_logo.raise_()

    # 登录表单内容部分
    login_widget = QWidget(self)
    login_widget.move(self.width/2 *0.8, 500)
    # login_widget.setGeometry(0, 140, 650, 260)
  
    hbox = QHBoxLayout()
    # 添加左侧logo
    # logolb = QLabel(self)
    # logopix = QPixmap(icon_path)
    # logopix_scared = logopix.scaled(100, 100)
    # logolb.setPixmap(logopix_scared)
    # logolb.setAlignment(Qt.AlignCenter)
    # hbox.addWidget(logolb, 1)

    # 添加右侧表单
    fmlayout = QFormLayout()
    lb_name = QLabel("姓名")
    lb_name.setStyleSheet("QWidget{color:rgb(65, 113, 156);font-weight:500;background: transparent;font-size:30px;}")
    lb_name.setFont(QFont("Microsoft YaHei"))
    self.lb_name_edited = QLineEdit()
    self.lb_name_edited.setFixedWidth(270)
    self.lb_name_edited.setFixedHeight(38)
    
    lb_xuehao = QLabel("学号")
    lb_xuehao.setStyleSheet("QWidget{color:rgb(65, 113, 156);font-weight:500;background: transparent;font-size:30px;}")
    lb_xuehao.setFont(QFont("Microsoft YaHei"))
    self.lb_xuehao_edited = QLineEdit()
    # lb_xuehao_edited.setEchoMode(QLineEdit.Password)
    self.lb_xuehao_edited.setFixedWidth(270)
    self.lb_xuehao_edited.setFixedHeight(38)

    lb_teacher = QLabel("导师")
    lb_teacher.setStyleSheet("QWidget{color:rgb(65, 113, 156);font-weight:500;background: transparent;font-size:30px;}")
    lb_teacher.setFont(QFont("Microsoft YaHei"))
    self.lb_teacher_edited = QLineEdit()
    self.lb_teacher_edited.setFixedWidth(270)
    self.lb_teacher_edited.setFixedHeight(38)
  
    self.btn_login = QPushButton("确认")
    self.btn_login.setStyleSheet("QWidget{color:rgb(65, 113, 156);font-weight:500;background: transparent;font-size:30px;}")
    self.btn_login.setFixedWidth(270)
    self.btn_login.setFixedHeight(40)
    self.btn_login.setFont(QFont("Microsoft YaHei"))
    self.btn_login.setObjectName("login_btn")
    self.btn_login.setStyleSheet("#login_btn{background-color:#2c7adf;color:#fff;border:none;border-radius:4px;}")
    self.btn_login.clicked.connect(self.on_pushButton_enter_clicked)
    fmlayout.addRow(lb_name, self.lb_name_edited)
    fmlayout.addRow(lb_xuehao, self.lb_xuehao_edited)
    fmlayout.addRow(lb_teacher, self.lb_teacher_edited)
    fmlayout.addWidget(self.btn_login)
    hbox.setAlignment(Qt.AlignCenter)
    # 调整间距
    fmlayout.setHorizontalSpacing(20)
    fmlayout.setVerticalSpacing(12)
  
    hbox.addLayout(fmlayout, 2)
  
    login_widget.setLayout(hbox)
  
    self.center()
    self.show()
  
  def center(self):
    qr = self.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())

  def on_pushButton_enter_clicked(self):
          # 信息判断
          print("1")
          if self.lb_name_edited.text() == "":
              return
          if self.lb_xuehao_edited.text() == "":
              return
          if self.lb_teacher_edited.text() == "":
              return
          print("登录成功，开始使用电脑")
          print(self.lb_name_edited.text())
          #处理上次登机的信息
          read_info_and_add_to_csv()
          start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) # 获取当前时间
          log_path=resource_path("log.txt")
          print(log_path)
          with open(log_path,"a") as f:
              f.write(self.lb_name_edited.text() + "," +self.lb_xuehao_edited.text()+ "," +self.lb_teacher_edited.text()+","+start_time + "\n") 
          result = QMessageBox.information(self, 'info','please check your info',QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
          if result == QMessageBox.Yes:
              self.showMinimized()
              self.setWindowFlags(Qt.ToolTip)
              while(1):
                  #每隔60s记录一下时间，所以关机时间的误差在60s内
                  self.setWindowFlags(Qt.ToolTip)
                  time.sleep(60)
                  end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) # 获取当前时间
                  with open(log_path,"a") as f:
                      f.write("run,"+end_time +"\n")
          else:
              return
  
if __name__ == "__main__":
    app = QApplication(sys.argv)
    desktop =  app.desktop()
               #获取显示器分辨率大小
    screenRect = desktop.screenGeometry()
    height = screenRect.height()
    width = screenRect.width()
    print(width,height)
    ex = LoginForm()
    ex.setGeometry(desktop.screenGeometry(0))
 
    #   ex.showFullScreen()
    sys.exit(app.exec_())
