from PyQt6.QtWidgets import QMessageBox, QMainWindow

from retail_project.connectors.employee_connector import EmployeeConnector
from retail_project.Uis.EmployeeMainWindowEx import EmployeeMainWindowEx
from retail_project.Uis.LoginMainWindow import Ui_MainWindow

class LoginMainWindowEx(Ui_MainWindow):
    def __init__(self):
        pass

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.setupSignalAndSlot()
    def showWindow(self):
        self.MainWindow.show()
    def setupSignalAndSlot(self):
        self.pushButtonLogin.clicked.connect(self.process_login)
    def process_login(self):
        email=self.lineEditEmail.text()
        password=self.lineEditPassword.text()
        ec = EmployeeConnector()
        ec.connect()
        em = ec.login(email,password)
        if em == None:
            msg=QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText('Login failed, please check your account again')
            msg.setWindowTitle('Login failed!')
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        else:
            #msg = QMessageBox()
            #msg.setIcon(QMessageBox.Icon.Information)
            #msg.setText('Congratulations! Login sucessfull!!!')
            #msg.setWindowTitle('Login  Ok Ok')
            #msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        #msg.exec()
            self.gui_emp=EmployeeMainWindowEx()
            self.gui_emp.setupUi(QMainWindow())
            self.gui_emp.showWindow()
            self.MainWindow.close()