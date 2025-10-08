from retail_project.connectors.employee_connector import EmployeeConnector

ec=EmployeeConnector()
ec.connect()
em=ec.login("putin@gmail.com","123")
if em==None:
    print("Login Failed!")
else:
    print("Login succesful!")
    print(em)