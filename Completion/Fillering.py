from numpy import nan as NA
import pandas as pd

data = pd.DataFrame([[1., 6.5, 3.],
                     [2., NA, NA],
                     [NA, NA, NA],
                     [3, 6.5, 3.],
                     [4, 7.5, 7.],
                     [5, 2.5, 3.]])
print(data)
print("-"*10)
cleaned=data.fillna(data.mean()) # => Thay NA bằng giá trị trung bình của CỘT tương ứng
# cleaned=data.dropna(how='all') => Xóa hàng mà tất cả các giá trị đều la NA
print(cleaned)


