import pandas as pd


def top_3_items_by_value(df):
    """
    Trả về top 3 mặt hàng có tổng giá trị lớn nhất.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame chứa dữ liệu bán hàng với các cột:
        'ProductID' (hoặc tên mặt hàng),
        'UnitPrice', 'Quantity', 'Discount'.

    Returns
    -------
    List[Tuple]
        Danh sách 3 mặt hàng, mỗi mục là tuple: (ProductID, Tổng giá trị), sắp xếp giảm dần theo tổng giá trị.
    """
    # Tính tổng giá trị từng dòng
    df['Total'] = df['UnitPrice'] * df['Quantity'] * (1 - df['Discount'])

    # Tính tổng giá trị theo từng mặt hàng
    item_totals = df.groupby('ProductID')['Total'].sum()

    # Lấy top 3 mặt hàng có tổng giá trị lớn nhất
    top3 = item_totals.sort_values(ascending=False).head(3)

    # Trả về list of tuples (ProductID, Total)
    return list(top3.items())


# ------------------- Ví dụ sử dụng -------------------
df = pd.read_csv("../datasets/SalesTransactions/SalesTransactions.csv")

top_items = top_3_items_by_value(df)
print("Top 3 mặt hàng có tổng giá trị lớn nhất:", top_items)
