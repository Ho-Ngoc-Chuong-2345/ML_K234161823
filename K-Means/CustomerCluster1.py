import mysql.connector
from flask import Flask, render_template_string, send_file
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
import numpy as np
import webbrowser
from threading import Timer

app = Flask(__name__)

def getConnect(server, port, database, username, password):
    try:
        app.config['MYSQL_DATABASE_HOST'] = server
        app.config['MYSQL_DATABASE_PORT'] = port
        app.config['MYSQL_DATABASE_DB'] = database
        app.config['MYSQL_DATABASE_USER'] = username
        app.config['MYSQL_DATABASE_PASSWORD'] = password
        conn = mysql.connector.connect(
            host=server,
            port=port,
            database=database,
            user=username,
            password=password
        )
        if conn.is_connected():
            print("Kết nối MySQL thành công!")
        return conn
    except mysql.connector.Error as e:
        print("Error =", e)
    return None

def closeConnection(conn):
    if conn is not None and conn.is_connected():
        conn.close()

def queryDataset(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
    cursor.close()
    return df

conn = getConnect('localhost', 3306, 'salesdatabase', 'root', '@Obama123')

sql1 = "SELECT * FROM customer"
df1 = queryDataset(conn, sql1)
print(df1)

sql2 = """
SELECT DISTINCT customer.CustomerId, Age, Annual_Income, Spending_Score
FROM customer, customer_spend_score
WHERE customer.CustomerId = customer_spend_score.CustomerID
"""
df2 = queryDataset(conn, sql2)
df2.columns = ['CustomerId', 'Age', 'Annual Income', 'Spending Score']

def showHistogram(df, columns):
    plt.figure(1, figsize=(7,8))
    for i, column in enumerate(columns, 1):
        plt.subplot(3, 1, i)
        plt.subplots_adjust(hspace=0.5, wspace=0.5)
        sns.histplot(df[column], bins=32, kde=True)
        plt.title(f'Histogram of {column}')
    plt.show()

showHistogram(df2, df2.columns[1:])

def elbowMethod(df, columnsForElbow):
    X = df.loc[:, columnsForElbow].values
    inertia = []
    for n in range(1, 11):
        model = KMeans(n_clusters=n, init='k-means++', max_iter=500, random_state=42)
        model.fit(X)
        inertia.append(model.inertia_)
    plt.figure(1, figsize=(15,6))
    plt.plot(np.arange(1, 11), inertia, 'o')
    plt.plot(np.arange(1, 11), inertia, '--', alpha=0.5)
    plt.xlabel('Number of Clusters')
    plt.ylabel('Cluster sum of squared distances')
    plt.show()

columns = ['Age', 'Spending Score']
elbowMethod(df2, columns)

def runKMeans(X, cluster):
    model = KMeans(n_clusters=cluster, init='k-means++', max_iter=500, random_state=42)
    model.fit(X)
    labels = model.labels_
    centroids = model.cluster_centers_
    y_kmeans = model.fit_predict(X)
    return y_kmeans, centroids, labels

X = df2.loc[:, columns].values
cluster = 4
colors = ["red", "green", "blue", "purple", "black", "pink", "orange"]
y_kmeans, centroids, labels = runKMeans(X, cluster)
df2["Cluster"] = labels

def visualizeKMeans(X, y_kmeans, cluster, title, xLabel, yLabel, colors):
    plt.figure(figsize=(10, 10))
    for i in range(cluster):
        plt.scatter(X[y_kmeans == i, 0], X[y_kmeans == i, 1], s=100, c=colors[i], label='Cluster %i' % (i + 1))
    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.legend()
    plt.show()

visualizeKMeans(X, y_kmeans, cluster, "Clusters of Customers - Age X Spending Score", "Age", "Spending Score", colors)
columns = ["Annual Income", "Spending Score"]
elbowMethod(df2, columns)
X = df2.loc[:, columns].values
cluster = 5
y_kmeans, centroids, labels = runKMeans(X, cluster)
df2["cluster"] = labels
visualizeKMeans(X, y_kmeans, cluster, "Clusters of Customers - Annual Income X Spending Score", "Annual Income", "Spending Score", colors)
columns = ['Age', 'Annual Income', 'Spending Score']
elbowMethod(df2, columns)
X = df2.loc[:, columns].values
cluster = 6
y_kmeans, centroids, labels = runKMeans(X, cluster)
df2["cluster"] = labels

def visualize3DKmeans(df, columns, hover_data, cluster):
    fig = px.scatter_3d(df, x=columns[0], y=columns[1], z=columns[2], color='cluster', hover_data=hover_data, category_orders={"cluster": range(0, cluster)})
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    fig.show()

hover_data = df2.columns
visualize3DKmeans(df2, columns, hover_data, cluster)

def showCustomerByCluster(conn, df_clustered, cluster_col):
    print("\n========== DANH SÁCH KHÁCH HÀNG THEO CỤM ==========\n")
    for c in sorted(df_clustered[cluster_col].unique()):
        sql = f"""
            SELECT Id, CustomerId, Name, Gender, Age
            FROM customer
            WHERE CustomerId IN (
                SELECT CustomerId FROM customer_spend_score
                WHERE CustomerId IN {tuple(df_clustered[df_clustered[cluster_col] == c]['CustomerId'].tolist())}
            )
        """
        df_customers = queryDataset(conn, sql)
        print(f"🔹 Cluster {c} ({len(df_customers)} khách hàng):")
        print(df_customers)
        print()

print("\n==================== THỰC HIỆN TRUY XUẤT THEO CỤM ====================")
for k in [4, 5, 6]:
    print(f"\n--- ĐANG XỬ LÝ K = {k} ---")
    X = df2.loc[:, ['Age', 'Annual Income', 'Spending Score']].values
    y_kmeans, centroids, labels = runKMeans(X, k)
    df2['Cluster'] = labels
    showCustomerByCluster(conn, df2, 'Cluster')
closeConnection(conn)
print("\n ĐÃ HOÀN THÀNH TRUY XUẤT CHI TIẾT CÁC CỤM (K=4,5,6)")

def export_to_sql(df, filename="CustomerClusters.sql"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("DROP TABLE IF EXISTS customer_cluster;\n")
        f.write("""CREATE TABLE customer_cluster (
    CustomerId INT,
    Age INT,
    Annual_Income FLOAT,
    Spending_Score FLOAT,
    Cluster INT
);\n\n""")
        for _, row in df.iterrows():
            f.write(f"INSERT INTO customer_cluster VALUES ({row['CustomerId']}, {row['Age']}, {row['Annual Income']}, {row['Spending Score']}, {row['Cluster']});\n")
    return filename

def plot_elbow(df):
    X = df[['Age', 'Annual Income', 'Spending_Score']].values
    inertias = []
    for k in [4, 5, 6]:
        model = KMeans(n_clusters=k, init='k-means++', random_state=42)
        model.fit(X)
        inertias.append(model.inertia_)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[4, 5, 6], y=inertias, mode='lines+markers'))
    fig.update_layout(title="Biểu đồ Elbow (k = 4,5,6)", xaxis_title="Số cụm (k)", yaxis_title="Inertia")
    return fig.to_html(full_html=False)

def plot_scatter2d(df):
    fig = px.scatter(df, x='Annual Income', y='Spending Score', color='Cluster', title="Phân cụm 2D: Annual Income vs Spending Score", template='plotly_white')
    return fig.to_html(full_html=False)

def plot_scatter3d(df):
    fig = px.scatter_3d(df, x='Age', y='Annual Income', z='Spending_Score', color='Cluster', title="Phân cụm 3D: Age - Income - Score", template='plotly_white')
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=30))
    return fig.to_html(full_html=False)

@app.route('/')
def index():
    clusters = {}
    for k in [4, 5, 6]:
        df_k = df2.copy()
        X = df_k[['Age', 'Annual Income', 'Spending_Score']].values
        y_kmeans, centroids, labels = runKMeans(X, k)
        df_k['Cluster'] = labels
        clusters[k] = df_k
    elbow_chart = plot_elbow(df2)
    scatter2d_chart = plot_scatter2d(clusters[5])
    scatter3d_chart = plot_scatter3d(clusters[6])
    export_to_sql(clusters[6])
    tables_html = ""
    for k, dfk in clusters.items():
        tables_html += f"<h4>Kết quả phân cụm k = {k}</h4>"
        tables_html += dfk.to_html(classes='table table-striped table-bordered', index=False, border=0)
    html = """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <title>Phân Cụm Khách Hàng</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background: #f6f7fb; font-family: 'Segoe UI', sans-serif; padding: 20px; }
            .container { background: #fff; padding: 30px; border-radius: 10px;
                         box-shadow: 0 4px 10px rgba(0,0,0,0.1); max-width: 1200px; margin: auto; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2 class="text-center mb-4">Phân Cụm Khách Hàng Bằng K-Means (k=4,5,6)</h2>
            <h4>Biểu đồ Elbow</h4>{{ elbow_chart|safe }}<hr>
            <h4>Biểu đồ 2D</h4>{{ scatter2d_chart|safe }}<hr>
            <h4>Biểu đồ 3D</h4>{{ scatter3d_chart|safe }}<hr>
            <a href="/download_sql" class="btn btn-warning">Tải file SQL</a>
            <h3 class="mt-4">Kết quả chi tiết</h3>{{ tables_html|safe }}
        </div>
    </body>
    </html>
    """
    return render_template_string(html, elbow_chart=elbow_chart, scatter2d_chart=scatter2d_chart, scatter3d_chart=scatter3d_chart, tables_html=tables_html)

@app.route('/download_sql')
def download_sql():
    return send_file("CustomerClusters.sql", as_attachment=True)

if __name__ == '__main__':
    Timer(1, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(debug=False)
