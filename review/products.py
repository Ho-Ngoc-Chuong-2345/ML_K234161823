class ListProduct:
    def __init__(self):
        self.products = []
    def add_product(self,p):
        self.products.append(p)
    def print_products(self):
        for p in self.products:
            print(p)

    def desc_sort_products(self):
        for i in range(0,len(self.products)):
            for j in range (i+1, len(self.products)):
                pi = self.products[i]
                pj = self.products[j]
                if pi.price < pj.price:
                    self.products[j] = pi
                    self.products[i] = pj

    def desc_sort_products_2(self):
        # Sắp xếp trực tiếp theo price giảm dần
        self.products.sort(key=lambda p: p.price, reverse=True)


