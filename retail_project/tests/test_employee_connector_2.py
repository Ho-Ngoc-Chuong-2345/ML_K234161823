from ML_K234161823.SQL.TestQueryMySQL import dataset
from retail_project.connectors.employee_connector import EmployeeConnector
from retail_project.models.employee import Employee

ec=EmployeeConnector()
ec.connect()
emp=Employee()
emp.EmployeeCode="EMP888"
emp.Name="Doraemon"
emp.Password="123"
emp.IsDeleted=0
emp.Phone="13230131423"
emp.email="ghwoie@gmail.com"
result =ec.insert_one_employee(emp)
if result>0:
    print("Chúc mừng nha, đã thêm thành công")
else:
    print("Thật đáng thương")
