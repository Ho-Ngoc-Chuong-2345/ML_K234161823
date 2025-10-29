from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox

from retail_project.connectors.employee_connector import EmployeeConnector
from retail_project.models.employee import Employee
from retail_project.Uis.EmployeeMainWindow import Ui_MainWindow


class EmployeeMainWindowEx(Ui_MainWindow):
    def __init__(self):
        self.ec = EmployeeConnector()
        self.ec.connect()
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.displayEmployeesIntoTable()
        self.is_completed = True
        self.setupSignalAndSlot()
    def showWindow(self):
        self.MainWindow.show()
    def displayEmployeesIntoTable(self):
        self.employees=self.ec.get_all_employee()
        #remove existing data:
        self.tableWidgetEmployee.setRowCount(0)
        #loading emp into table:
        for emp in self.employees:
            #get the last row (for appending):
            row=self.tableWidgetEmployee.rowCount()
            #insert a new row (at the last row):
            self.tableWidgetEmployee.insertRow(row)
            #insert data for ID column (of row)
            item_id=QTableWidgetItem(str(emp.ID))
            self.tableWidgetEmployee.setItem(row,0,item_id)
            if emp.IsDeleted ==1:
                item_id.setBackground(Qt.GlobalColor.red)
            #Code:
            item_code=QTableWidgetItem(str(emp.EmployeeCode))
            self.tableWidgetEmployee.setItem(row,1,item_code)
            #Name
            item_name=QTableWidgetItem(emp.Name)
            self.tableWidgetEmployee.setItem(row,2,item_name)
            #Phone
            item_phone=QTableWidgetItem(emp.Phone)
            self.tableWidgetEmployee.setItem(row,3,item_phone)
            #Email
            item_email=QTableWidgetItem(emp.Email)
            self.tableWidgetEmployee.setItem(row,4,item_email)
    def setupSignalAndSlot(self):
        self.pushButtonNew.clicked.connect(self.clear_all)
        self.tableWidgetEmployee.itemSelectionChanged.connect(self.show_detail)
        self.pushButtonSave.clicked.connect(self.save_employee)
        self.pushButtonUpdate.clicked.connect(self.update_employee)
        self.pushButtonDelete.clicked.connect(self.delete_employee)
    def clear_all(self):
        self.lineEditId.setText("")
        self.lineEditCode.clear()
        self.lineEditName.setText("")
        self.lineEditPhone.setText("")
        self.lineEditEmail.setText("")
        self.lineEditCode.setFocus()
    def show_detail(self):
        if self.is_completed==False:
            return
        row_index=self.tableWidgetEmployee.currentIndex()
        print("you clicked at ",row_index.row())
        id=self.tableWidgetEmployee.item(row_index.row(),0).text()
        print("Employee ID=",id)
        emp=self.ec.get_detail_infor(id)
        if emp!=None:
            self.lineEditId.setText(str(emp.ID))
            self.lineEditCode.setText(str(emp.EmployeeCode))
            self.lineEditName.setText(emp.Name)
            self.lineEditPhone.setText(emp.Phone)
            self.lineEditEmail.setText(emp.Email)
            if emp.IsDeleted==1:
                self.checkBoxIsDeleted.setChecked(True)
            else:
                self.checkBoxIsDeleted.setChecked(False)
    def save_employee(self):
        emp = Employee()
        emp.EmployeeCode = self.lineEditCode.text()
        emp.Name = self.lineEditName.text()
        emp.Phone = self.lineEditPhone.text()
        emp.Email = self.lineEditEmail.text()
        emp.Password = self.lineEditPassword.text()
        emp.IsDeleted = 0

        result = self.ec.insert_one_employee(emp)
        if result > 0:
            self.displayEmployeesIntoTable()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Thương quá ... ko có lưu được")
            msg.setWindowTitle("Lưu lỗi tè le")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        self.is_completed=True
    def update_employee(self):
        self.is_completed=False
        emp = Employee()
        emp.ID = self.lineEditId.text()
        emp.EmployeeCode = self.lineEditCode.text()
        emp.Name = self.lineEditName.text()
        emp.Phone = self.lineEditPhone.text()
        emp.Email = self.lineEditEmail.text()
        emp.Password = self.lineEditPassword.text()
        if self.checkBoxIsDeleted.isChecked() == True:
            emp.IsDeleted = 1
        else:
            emp.IsDeleted = 0
        result = self.ec.insert_one_employee(emp)
        if result > 0:
            self.displayEmployeesIntoTable()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Thương quá ... ko xóa được")
            msg.setWindowTitle("Xóa lỗi tè le")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        self.is_completed=True

    def Deleted_emp(self):
        self.is_completed = False
        emp = Employee()
        emp.ID = self.lineEditEmpID.text()
        result = self.ec.deletedOneEmployee(emp)
        if result > 0:
            self.displayListEmployee()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Không xóa được rồi")
            msg.setWindowTitle("Lưu lỗi tè le")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        self.is_completed = True




