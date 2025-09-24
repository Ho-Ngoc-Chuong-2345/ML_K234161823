from review.product import Product

p1 = Product(100,"Thuốc Lào", 4,20)
# Xuất p1 ra màn hình:
print(p1)

p2=Product(200,"Thuốc trị hôi nách",5,10)
p1=p2
print("Thông tin của p1 là:")
print(p1)
p1.name = "Thuốc tăng tự trọng"
print("Thông tin của p2 là:" )
print(p2)
