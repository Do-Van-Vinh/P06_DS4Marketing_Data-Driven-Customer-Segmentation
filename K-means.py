Họ và tên: Đỗ Văn Vinh
Mã sinh viên: 2121051277
Nhóm: Thương mại điện tử _07
# Tải dữ liệu
import pandas as pd
df = pd.read_excel('Online Retail.xlsx', sheet_name='Online Retail')

#-------------------------------Dọn Dẹp Dữ Liệu-------------------------------
    #1.Loại bỏ các đơn hàng đã huỷ
df = df.loc[df['Quantity']>0]
    #2.Loại bỏ  các bản ghi không có CustomerID
df = df[pd.notnull(df['CustomerID'])]    
    #3.Loại trừ 1 tháng không đầy đủ
df = df.loc[df['InvoiceDate'] < '2011-12-01' ]    
    #4.Tính tổng doanh số bán hàng từ cột Quantity và UnitPrice
df [ 'Sales' ] = df [ 'Quantity' ] * df[ 'UnitPrice' ]    
    #5.Dữ liệu theo khách hàng 
customer_df = df.groupby ( 'CustomerID' ).agg({
	'Sales' : sum,
	'InvoiceNo' : lambda x: x.nunique ()
}) 
customer_df.columns = ['TotalSales','OrderCount' ]
customer_df['AvgOrderValue']=customer_df['TotalSales']/customer_df['OrderCount']
    #Chuẩn hoá dữ liệu ở cùng một tỷ lệ
rank_df = customer_df.rank ( method = 'first' )
    #Giá trị trung bình bằng 0 và độ lệch chuẩn là 1
normalized_df=(rank_df-rank_df.mean()) / rank_df.std()

#-------------------------------Phân Cụm K-means-------------------------------
from sklearn.cluster import KMeans
    # K-means
kmeans = KMeans(n_clusters=4).fit(normalized_df[['TotalSales', 'OrderCount', 'AvgOrderValue']])    
four_cluster_df = normalized_df[['TotalSales','OrderCount','AvgOrderValue']].copy(deep=True)
four_cluster_df['Cluster'] = kmeans.labels_
# OderCount và TotalSales
import matplotlib.pyplot as plt
plt.scatter(
	four_cluster_df.loc[four_cluster_df['Cluster'] == 0]['OrderCount'],
	four_cluster_df.loc[four_cluster_df['Cluster'] == 0]['TotalSales'],
	c = 'blue'
)
plt.scatter(
	four_cluster_df.loc[four_cluster_df['Cluster'] == 1]['OrderCount'],
	four_cluster_df.loc[four_cluster_df['Cluster'] == 1]['TotalSales'],
	c = 'red'
)
plt.scatter(
	four_cluster_df.loc[four_cluster_df['Cluster'] == 2]['OrderCount'],
	four_cluster_df.loc[four_cluster_df['Cluster'] == 2]['TotalSales'],
	c = 'orange'
)
plt.scatter(
	four_cluster_df.loc[four_cluster_df['Cluster'] == 3]['OrderCount'],
	four_cluster_df.loc[four_cluster_df['Cluster'] == 3]['TotalSales'],
	c = 'green'
)
plt.title ('TotalSales vs. OrderCount Clusters')
plt.xlabel ('Order Count')
plt.ylabel ('Tatal Sales')

plt.grid()
plt.show()

# OderCount và AvgOrderValue
plt.scatter(
	four_cluster_df.loc[four_cluster_df['Cluster'] == 0]['OrderCount'],
	four_cluster_df.loc[four_cluster_df['Cluster'] == 0]['AvgOrderValue'],
	c = 'blue'
)
plt.scatter(
	four_cluster_df.loc[four_cluster_df['Cluster'] == 1]['OrderCount'],
	four_cluster_df.loc[four_cluster_df['Cluster'] == 1]['AvgOrderValue'],
	c = 'red'
)
plt.scatter(
	four_cluster_df.loc[four_cluster_df['Cluster'] == 2]['OrderCount'],
	four_cluster_df.loc[four_cluster_df['Cluster'] == 2]['AvgOrderValue'],
	c = 'orange'
)
plt.scatter(
	four_cluster_df.loc[four_cluster_df['Cluster'] == 3]['OrderCount'],
	four_cluster_df.loc[four_cluster_df['Cluster'] == 3]['AvgOrderValue'],
	c = 'green'
)
plt.title ('AvgOrderValue vs. OrderCount Clusters')
plt.xlabel ('Order Count')
plt.ylabel ('AvgOrderValue')

plt.grid()
plt.show()

# TatalSales và AvgOrderValue 
plt.scatter(
	four_cluster_df.loc[four_cluster_df['Cluster'] == 0]['TotalSales'],
	four_cluster_df.loc[four_cluster_df['Cluster'] == 0]['AvgOrderValue'],
	c = 'blue'
)
plt.scatter(
	four_cluster_df.loc[four_cluster_df['Cluster'] == 1]['TotalSales'],
	four_cluster_df.loc[four_cluster_df['Cluster'] == 1]['AvgOrderValue'],
	c = 'red'
)
plt.scatter(
	four_cluster_df.loc[four_cluster_df['Cluster'] == 2]['TotalSales'],
	four_cluster_df.loc[four_cluster_df['Cluster'] == 2]['AvgOrderValue'],
	c = 'orange'
)
plt.scatter(
	four_cluster_df.loc[four_cluster_df['Cluster'] == 3]['TotalSales'],
	four_cluster_df.loc[four_cluster_df['Cluster'] == 3]['AvgOrderValue'],
	c = 'green'
)
plt.title ('TotalSales vs. AvgOrderValue Clusters')
plt.xlabel ('TotalSales')
plt.ylabel ('AvgOrderValue')

plt.grid()
plt.show()  
#---------------------------Lựa Chọn Số Cụm Tốt Nhất---------------------------
from sklearn.metrics import silhouette_score
for n_cluster in [4,5,6,7,8]: 
	kmeans = KMeans(n_clusters = n_cluster).fit(
		normalized_df[['TotalSales', 'OrderCount', 'AvgOrderValue']] )
	silhouette_avg = silhouette_score (
		normalized_df[['TotalSales', 'OrderCount', 'AvgOrderValue']],
		kmeans.labels_ )
	print (' Silhouette Score for %i Clusters: %0.4f ' % (n_cluster, silhouette_avg))
#----------------------Giải thích các phân khúc khách hàng---------------------
# Điều chỉnh mô hình phân cụm k-means với 4 cụm   
kmeans = KMeans(n_clusters=4).fit(normalized_df[['TotalSales','OrderCount','AvgOrderValue']] )
four_cluster_df = normalized_df[['TotalSales', 'OrderCount','AvgOrderValue']].copy(deep=True)
four_cluster_df['Cluster'] = kmeans.labels_
# Lấy tâm cụm
kmeans.labels_
kmeans.cluster_centers_
# Tìm hiểu mặt hàng bán chạy nhất
high_value_cluster = four_cluster_df.loc[four_cluster_df['Cluster'] == 2]
pd.DataFrame(
	df.loc[
		df['CustomerID'].isin(high_value_cluster.index)
		].groupby('Description').count()[ 'StockCode'
		].sort_values(ascending=False).head()
)
