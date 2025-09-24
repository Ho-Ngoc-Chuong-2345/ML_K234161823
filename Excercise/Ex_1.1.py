import pandas as pd


def get_orders_in_range(df, minValue, maxValue, SortType=True):
    """
    Lọc và sắp xếp các hóa đơn theo tổng giá trị.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame chứa dữ liệu hóa đơn với các cột: 'OrderID', 'UnitPrice', 'Quantity', 'Discount'.
    minValue : float
        Giá trị tối thiểu của tổng hóa đơn.
    maxValue : float
        Giá trị tối đa của tổng hóa đơn.
    SortType : bool, default True
        Kiểu sắp xếp theo tổng giá trị:
        - True: sắp xếp tăng dần
        - False: sắp xếp giảm dần

    Returns
    -------
    List[Tuple]
        Danh sách các hóa đơn, mỗi hóa đơn là tuple: (OrderID, Tổng giá trị), đã lọc theo [minValue, maxValue]
        và sắp xếp theo SortType.
    """
    # Tính tổng giá trị từng dòng
    df['Total'] = df['UnitPrice'] * df['Quantity'] * (1 - df['Discount'])

    # Tính tổng giá trị theo từng OrderID
    order_totals = df.groupby('OrderID')['Total'].sum()

    # Lọc theo khoảng minValue ... maxValue
    filtered_orders = order_totals[(order_totals >= minValue) & (order_totals <= maxValue)]

    # Sắp xếp theo SortType
    sorted_orders = filtered_orders.sort_values(ascending=SortType)

    # Trả về dạng list of tuples (OrderID, Total)
    result = list(sorted_orders.items())

    return result


# ------------------- Ví dụ sử dụng -------------------
df = pd.read_csv("../datasets/SalesTransactions/SalesTransactions.csv")

minValue = float(input("Nhập tổng giá trị min: "))
maxValue = float(input("Nhập tổng giá trị max: "))
SortType = True  # True = tăng dần, False = giảm dần

results = get_orders_in_range(df, minValue, maxValue, SortType)
print("Danh sách hóa đơn lọc và sắp xếp:", results)
