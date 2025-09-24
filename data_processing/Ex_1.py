import pandas as pd

def find_orders_within_range(df, minValue, maxValue):
    # Tổng giá trị từng đơn hàng
    order_totals = df.groupby('OrderID').apply(
        lambda x: (x['UnitPrice'] * x['Quantity'] * (1 - x['Discount'])).sum())
    # Lọc các đơn hàng trong range
    orders_within_range = order_totals[(order_totals >= minValue) & (order_totals <= maxValue)]
    # Danh sách mã đơn hàng không trùng lặp
    unique_orders = orders_within_range.index.tolist()
    return unique_orders

df = pd.read_csv("../datasets/SalesTransactions/SalesTransactions.csv")

minValue = float(input("Nhập giá trị min: "))
maxValue = float(input("Nhập giá trị max: "))
results = find_orders_within_range(df, minValue, maxValue)
print("Danh sách các hóa đơn trong phạm vi giá trị từ", minValue, "đến", maxValue, "là", results)
