# 1. Pointwise Approach
# =====================
# Ý tưởng: Xem bài toán xếp hạng như một bài toán regression/classification
# Mỗi query-document có nhãn relevance (mức độ liên quan)
# => Dự đoán điểm số và sắp xếp theo điểm

import pandas as pd
from sklearn.linear_model import LinearRegression

# Data nhỏ: query, feature (giả sử TF-IDF), relevance
data = {
    "query": ["q1", "q1", "q1", "q2", "q2"],
    "feature": [0.1, 0.3, 0.2, 0.5, 0.7],
    "relevance": [0, 1, 0, 1, 2]   # relevance score
}
df = pd.DataFrame(data)

# Train mô hình regression dự đoán relevance
X = df[["feature"]]
y = df["relevance"]
model = LinearRegression().fit(X, y)

# Dự đoán
df["pred_score"] = model.predict(X)

# Xếp hạng trong từng query
df["rank"] = df.groupby("query")["pred_score"].rank(ascending=False)

print("Pointwise Result:")
print(df)

# 2. Pairwise Approach
# ====================
# Ý tưởng: Xem xếp hạng như một bài toán phân loại nhị phân
# Với mỗi cặp tài liệu (d1, d2) cho cùng một query:
#   - Nếu d1 "quan trọng hơn" d2 => label = 1
#   - Ngược lại => label = 0
# Mô hình học để dự đoán tài liệu nào "thắng" trong cặp.

from itertools import combinations
from sklearn.linear_model import LogisticRegression

# Sinh dữ liệu cặp từ df
pairs = []
labels = []
for q in df["query"].unique():
    docs = df[df["query"] == q]
    for (i1, row1), (i2, row2) in combinations(docs.iterrows(), 2):
        # tạo feature = chênh lệch giữa 2 tài liệu
        feat = row1["feature"] - row2["feature"]
        label = 1 if row1["relevance"] > row2["relevance"] else 0
        pairs.append([feat])
        labels.append(label)

X_pair = pd.DataFrame(pairs, columns=["feat_diff"])
y_pair = labels

# Train logistic regression
clf = LogisticRegression().fit(X_pair, y_pair)

print("\nPairwise Result (trained on feature differences):")
print(X_pair.head())
print("Labels:", y_pair[:5])


# 3. Listwise Approach
# ====================
# Ý tưởng: Xem toàn bộ danh sách tài liệu ứng với 1 query
# Tối ưu trực tiếp một hàm loss dựa trên metric xếp hạng (NDCG, MAP,...)
# Ví dụ đơn giản: dùng Gradient Boosting Ranker trong sklearn (XGBRanker phổ biến hơn).

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

# Chuẩn bị dữ liệu: tương tự pointwise
X = df[["feature"]]
y = df["relevance"]

# Train với regressor (mô phỏng listwise, thực tế dùng XGBoost Ranker, LightGBM Ranker)
listwise_model = GradientBoostingRegressor().fit(X, y)
df["listwise_score"] = listwise_model.predict(X)

# Xếp hạng theo query
df["listwise_rank"] = df.groupby("query")["listwise_score"].rank(ascending=False)

print("\nListwise Result:")
print(df[["query", "feature", "relevance", "listwise_score", "listwise_rank"]])

