from ML_K234161823.SQL.TestQueryMySQL import dataset
from retail_project.connectors.employee_connector import EmployeeConnector

ec=EmployeeConnector()
ec.connect()
em=ec.login("putin@gmail.com","123")
if em==None:
    print("Login Failed!")
else:
    print("Login succesful!")
    print(em)


#Test get all employee
print("List of Employees:")
ds = ec.get_all_employee()
print(ds)

for emp in ds:
    print(emp)

id=3
emp=ec.get_detail_infor(id)
if emp==None:
    print("Không có nhân viên nào có mã = ", id)
else:
    print("Tìm thấy nhân viên có mã = ", id)
    print(id)


result=ec.delete_one_employee(emp)
if result>0:
    print('Chúc mung ban đã xóa thành công')
else:
    print("Xu")