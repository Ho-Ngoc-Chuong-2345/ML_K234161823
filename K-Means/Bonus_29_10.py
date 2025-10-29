"""
Sakila Customer Analytics
(1) Phân loại khách hàng theo Tên phim
(2) Phân loại khách hàng theo Category
(3) K-Means gom cụm khách hàng theo mức độ quan tâm Film/Inventory
"""

import mysql.connector
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# ===================== Cấu hình kết nối =====================
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "sakila"
DB_USER = "root"
DB_PASS = "@Obama123"

# ===================== Kết nối & tiện ích =====================
def get_connect():
    conn = mysql.connector.connect(
        host=DB_HOST, port=DB_PORT, database=DB_NAME,
        user=DB_USER, password=DB_PASS
    )
    return conn

def query_df(conn, sql, params=None):
    cur = conn.cursor()
    cur.execute(sql, params or ())
    if cur.description is None:
        cur.close()
        return pd.DataFrame()
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    cur.close()
    return pd.DataFrame(rows, columns=cols)


# ===================== (1) Khách hàng theo TÊN PHIM =====================
def customers_by_film_detail(conn):
    """
    Trả về từng dòng (film_title, customer_id, customer_name) — có thể trùng nếu 1 KH thuê nhiều inventory cùng film.
    Dùng DISTINCT để loại trùng ở mức KH x Film.
    """
    sql = """
    SELECT DISTINCT
        f.film_id,
        f.title AS film_title,
        c.customer_id,
        CONCAT(c.first_name, ' ', c.last_name) AS customer_name
    FROM rental r
    JOIN inventory i   ON r.inventory_id = i.inventory_id
    JOIN film f        ON i.film_id = f.film_id
    JOIN customer c    ON r.customer_id = c.customer_id
    ORDER BY f.title, customer_name;
    """
    return query_df(conn, sql)

def customers_by_film_aggregated(conn):
    """
    Gộp danh sách khách hàng (đã loại trùng) theo từng phim bằng GROUP_CONCAT.
    """
    # tăng giới hạn độ dài group_concat để không bị cắt
    query_df(conn, "SET SESSION group_concat_max_len = 1024*1024;")

    sql = """
    SELECT
        f.film_id,
        f.title AS film_title,
        COUNT(DISTINCT r.customer_id) AS total_customers,
        GROUP_CONCAT(DISTINCT CONCAT(c.first_name, ' ', c.last_name) ORDER BY c.last_name, c.first_name SEPARATOR ', ') AS customers
    FROM rental r
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN film f      ON i.film_id = f.film_id
    JOIN customer c  ON r.customer_id = c.customer_id
    GROUP BY f.film_id, f.title
    ORDER BY f.title;
    """
    return query_df(conn, sql)

# ===================== (2) Khách hàng theo CATEGORY =====================
def customers_by_category_detail(conn):
    """
    Trả về từng dòng (category_name, customer_id, customer_name), DISTINCT để loại trùng khách nếu họ thuê nhiều film cùng category.
    """
    sql = """
    SELECT DISTINCT
        cat.category_id,
        cat.name AS category_name,
        c.customer_id,
        CONCAT(c.first_name, ' ', c.last_name) AS customer_name
    FROM rental r
    JOIN inventory i     ON r.inventory_id = i.inventory_id
    JOIN film f          ON i.film_id = f.film_id
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category cat     ON fc.category_id = cat.category_id
    JOIN customer c       ON r.customer_id = c.customer_id
    ORDER BY cat.name, customer_name;
    """
    return query_df(conn, sql)

def customers_by_category_aggregated(conn):
    """
    Gộp danh sách khách hàng theo Category (đã loại trùng).
    """
    query_df(conn, "SET SESSION group_concat_max_len = 1024*1024;")
    sql = """
    SELECT
        cat.category_id,
        cat.name AS category_name,
        COUNT(DISTINCT r.customer_id) AS total_customers,
        GROUP_CONCAT(DISTINCT CONCAT(c.first_name, ' ', c.last_name) ORDER BY c.last_name, c.first_name SEPARATOR ', ') AS customers
    FROM rental r
    JOIN inventory i      ON r.inventory_id = i.inventory_id
    JOIN film f           ON i.film_id = f.film_id
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category cat     ON fc.category_id = cat.category_id
    JOIN customer c       ON r.customer_id = c.customer_id
    GROUP BY cat.category_id, cat.name
    ORDER BY cat.name;
    """
    return query_df(conn, sql)

# ===================== (3) K-Means: đề xuất features =====================
def build_customer_features(conn):
    """
    Đề xuất các thuộc tính phản ánh 'mức độ quan tâm Film/Inventory':
      - total_rentals: tổng số lượt thuê
      - unique_films: số film khác nhau
      - unique_categories: số category khác nhau
      - distinct_stores: số cửa hàng (store) KH từng thuê
      - avg_rental_duration_days: thời lượng mượn trung bình (ngày)
      - span_days: khoảng thời gian từ lần thuê đầu -> cuối (ngày)
      - rentals_per_month: nhịp độ thuê ≈ total_rentals / (span_days/30) (nếu span_days > 0)
    """
    sql = """
    WITH base AS (
        SELECT
            c.customer_id,
            r.rental_id,
            r.rental_date,
            r.return_date,
            i.film_id,
            i.store_id
        FROM customer c
        JOIN rental r   ON c.customer_id = r.customer_id
        JOIN inventory i ON r.inventory_id = i.inventory_id
    ),
    cat_map AS (
        SELECT DISTINCT f.film_id, fc.category_id
        FROM film f
        JOIN film_category fc ON f.film_id = fc.film_id
    )
    SELECT
        b.customer_id,
        COUNT(*) AS total_rentals,
        COUNT(DISTINCT b.film_id) AS unique_films,
        COUNT(DISTINCT cm.category_id) AS unique_categories,
        COUNT(DISTINCT b.store_id) AS distinct_stores,
        AVG(DATEDIFF(b.return_date, b.rental_date)) AS avg_rental_duration_days,
        DATEDIFF(MAX(b.rental_date), MIN(b.rental_date)) AS span_days
    FROM base b
    LEFT JOIN cat_map cm ON b.film_id = cm.film_id
    GROUP BY b.customer_id
    ORDER BY b.customer_id;
    """
    df = query_df(conn, sql)

    # rentals_per_month (ổn định khi span_days > 0)
    df["rentals_per_month"] = np.where(
        df["span_days"] > 0,
        df["total_rentals"] / (df["span_days"] / 30.0),
        df["total_rentals"]
    )

    # điền NA (nếu khách chưa trả phim -> avg có thể NA)
    df["avg_rental_duration_days"] = df["avg_rental_duration_days"].fillna(df["avg_rental_duration_days"].median())

    return df

def run_kmeans(df_features, k=5, random_state=42):
    """
    Chuẩn hóa feature và chạy KMeans.
    """
    feature_cols = [
        "total_rentals", "unique_films", "unique_categories",
        "distinct_stores", "avg_rental_duration_days",
        "span_days", "rentals_per_month"
    ]
    X = df_features[feature_cols].values.astype(float)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    km = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=random_state)
    labels = km.fit_predict(X_scaled)

    out = df_features.copy()
    out["cluster"] = labels
    return out, km, scaler, feature_cols

def elbow_plot(df_features, ks=range(2, 9)):
    feature_cols = [
        "total_rentals", "unique_films", "unique_categories",
        "distinct_stores", "avg_rental_duration_days",
        "span_days", "rentals_per_month"
    ]
    X = df_features[feature_cols].values.astype(float)
    X = StandardScaler().fit_transform(X)
    inertias = []
    for k in ks:
        km = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42)
        km.fit(X)
        inertias.append(km.inertia_)
    plt.figure(figsize=(7,4))
    plt.plot(list(ks), inertias, marker="o")
    plt.title("Elbow: chọn k")
    plt.xlabel("k")
    plt.ylabel("Inertia")
    plt.tight_layout()
    plt.show()

# ===================== Main chạy thử =====================
if __name__ == "__main__":
    conn = get_connect()
    print(" Đã kết nối MySQL/Sakila")

    # ---- (1) theo phim
    df_film_detail = customers_by_film_detail(conn)
    df_film_agg = customers_by_film_aggregated(conn)
    df_film_detail.to_csv("customers_by_film_detail.csv", index=False, encoding="utf-8")
    df_film_agg.to_csv("customers_by_film_aggregated.csv", index=False, encoding="utf-8")
    print(f"(1) Theo TÊN PHIM: {len(df_film_detail)} dòng chi tiết, {len(df_film_agg)} phim (đã gộp).")

    # ---- (2) theo category
    df_cat_detail = customers_by_category_detail(conn)
    df_cat_agg = customers_by_category_aggregated(conn)
    df_cat_detail.to_csv("customers_by_category_detail.csv", index=False, encoding="utf-8")
    df_cat_agg.to_csv("customers_by_category_aggregated.csv", index=False, encoding="utf-8")
    print(f"(2) Theo CATEGORY: {len(df_cat_detail)} dòng chi tiết, {len(df_cat_agg)} category (đã gộp).")

    # ---- (3) Features + KMeans
    df_feat = build_customer_features(conn)
    print("(3) Mẫu features:\n", df_feat.head())

    # Tùy bạn xem elbow để chọn k:
    # elbow_plot(df_feat, ks=range(2, 9))

    clustered, km, scaler, feature_cols = run_kmeans(df_feat, k=5, random_state=42)
    clustered.to_csv("customer_clusters.csv", index=False, encoding="utf-8")
    print("👥 Phân bố cụm:\n", clustered["cluster"].value_counts().sort_index())

    # Xuất SQL tạo bảng kết quả (nếu muốn nhập lại DB)
    with open("customer_clusters.sql", "w", encoding="utf-8") as f:
        f.write("DROP TABLE IF EXISTS customer_cluster;\n")
        f.write("""CREATE TABLE customer_cluster (
  customer_id SMALLINT UNSIGNED NOT NULL,
  total_rentals INT,
  unique_films INT,
  unique_categories INT,
  distinct_stores INT,
  avg_rental_duration_days DECIMAL(10,2),
  span_days INT,
  rentals_per_month DECIMAL(10,2),
  cluster TINYINT
);\n\n""")
        for _, r in clustered.iterrows():
            f.write(
                "INSERT INTO customer_cluster VALUES "
                f"({int(r.customer_id)},{int(r.total_rentals)},{int(r.unique_films)},{int(r.unique_categories)},"
                f"{int(r.distinct_stores)},{float(r.avg_rental_duration_days):.2f},{int(r.span_days)},"
                f"{float(r.rentals_per_month):.2f},{int(r.cluster)});\n"
            )

    conn.close()
    print("\n Hoàn tất. Đã tạo các file:")
    print(" - customers_by_film_detail.csv")
    print(" - customers_by_film_aggregated.csv")
    print(" - customers_by_category_detail.csv")
    print(" - customers_by_category_aggregated.csv")
    print(" - customer_clusters.csv")
    print(" - customer_clusters.sql")
