from review.product import Product
from review.products import ListProduct

lp=ListProduct()
lp.add_product(Product(100,"Product 1", 200, 10))
lp.add_product(Product(100,"Product 2", 10, 12))
lp.add_product(Product(100,"Product 3", 80, 5))
lp.add_product(Product(100,"Product 4", 50, 21))
lp.add_product(Product(100,"Product 5", 150, 15))
lp.add_product(Product(100,"Product 6", 200, 16))

print ("List of Products:")
lp.print_products()

lp.desc_sort_products()
print("List of Products after descending sort:")
lp.print_products()


lp.desc_sort_products_2()
print("List of Products after descending sort_2:")
lp.print_products()