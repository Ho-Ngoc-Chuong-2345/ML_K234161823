from PyQt6.QtWidgets import QMainWindow, QApplication

from retail_project.Uis.LoginMainWindowEx import LoginMainWindowEx

app=QApplication([])
login_ui=LoginMainWindowEx()
login_ui.setupUi(QMainWindow())
login_ui.showWindow()
app.exec()