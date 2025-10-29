from ML_K234161823.SQL.TestQueryMySQL import dataset
from retail_project.connectors.employee_connector import EmployeeConnector
from retail_project.models.employee import Employee

ec=EmployeeConnector()
ec.connect()
emp=Employee()
empID=7
emp.EmployeeCode="EMP992"
emp.Name="Chaien"
emp.Password="123"
emp.IsDeleted=0
emp.Phone="0981274174"
emp.email="ghwoie@gmail.com"
result =ec.insert_one_employee(emp)
if result>0:
    print("Đã sửa thành công")
else:
    print("Thật đáng thương")
