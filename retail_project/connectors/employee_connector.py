from scipy import datasets

from retail_project.connectors.connector import Connector
from retail_project.models.employee import Employee


class EmployeeConnector(Connector):
    def login(self,email,pwd):
        sql = "SELECT * FROM employee " \
              "where Email=%s and Password=%s"
        val = (email, pwd)
        dataset=self.fetchone(sql, val)
        if dataset==None:
            return None
        emp=Employee(dataset[0],
                     dataset[1],
                     dataset[2],
                     dataset[3],
                     dataset[4],dataset[5],dataset[6])
        return emp
    def get_all_employee(self):
        sql = "SELECT * FROM employee"
        dataset=self.fetchall(sql, None)
        print(dataset)
        employees = []
        for dataset in datasets:
            emp = Employee(dataset[0],
                           dataset[1],
                           dataset[2],
                           dataset[3],
                           dataset[4], dataset[5], dataset[6])
            employees.append(emp)
        return employees

    def get_detail_infor(self, id):
        sql = "SELECT * FROM employee " \
              "where Email=%s and Password=%s"
        val = (id,)
        dataset = self.fetchone(sql, val)
        if dataset == None:
            return None
        emp = Employee(dataset[0],
                       dataset[1],
                       dataset[2],
                       dataset[3],
                       dataset[4], dataset[5], dataset[6])
        return emp
    def insert_one_employee (self,emp):
        sql = "INSERT " \
              "INTO " \
              "employee " \
              "( " \
              "   `Name`, " \
              "   `Phone`, " \
              "   `Email`, " \
              "   `EmployeeCode`, " \
              "   `Password`, " \
              "   `IsDeleted` " \
              "VALUES (%s, %s, %s, %s, %s, %s)"
        val=(emp.EmployeeCode, emp.Name, emp.Phone, emp.Email,emp.Password,emp.IsDeleted)
        result=self.insert_one(sql,val)
        return result

    def delete_one_employee (self,emp):
        sql='delete from employee where ID=%s'
        val=(emp.ID,)
        result = self.insert_one(sql, val)
        return result

