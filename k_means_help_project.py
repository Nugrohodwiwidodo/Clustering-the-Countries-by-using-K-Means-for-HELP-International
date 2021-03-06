# -*- coding: utf-8 -*-
"""K-Means_HELP_Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NJW2iATttKhe1OMSDHnDw-LIAVOc20ID

#**Clustering the Countries by using K-Means for HELP International**

#Objective
Untuk mengkategorikan negara menggunakan faktor sosial ekonomi dan kesehatan yang menentukan pembangunan negara secara keseluruhan.

#Tentang Organisasi
HELP International adalah LSM kemanusiaan internasional yang berkomitmen untuk memerangi kemiskinan dan menyediakan fasilitas dan bantuan dasar bagi masyarakat di negara-negara terbelakang saat terjadi bencana dan bencana alam.

#Permasalahan
HELP International telah berhasil mengumpulkan sekitar $ 10 juta. Saat ini, CEO LSM perlu memutuskan bagaimana menggunakan uang ini secara strategis dan efektif. Jadi, CEO harus mengambil keputusan untuk memilih negara yang paling membutuhkan bantuan. Oleh karena itu, Tugasnyaadalah mengkategorikan negara menggunakan beberapa faktor sosial ekonomi dan kesehatan yang menentukan perkembangan negara secara keseluruhan. Kemudian perlu menyarankan negara mana saja  yang paling perlu menjadi fokus CEO.

#Kolom fitur
1. Negara : Nama negara
2. Kematian_anak: Kematian anak di bawah usia 5 tahun per 1000 kelahiran
3. Ekspor : Ekspor barang dan jasa perkapita
4. Kesehatan: Total pengeluaran kesehatan perkapita 
5. Impor: Impor barang dan jasa perkapita
6. Pendapatan: Penghasilan bersih perorang
7. Inflasi: Pengukuran tingkat pertumbuhan tahunan dari Total GDP 
8. Harapan_hidup: Jumlah tahun rata-rata seorang anak yang baru lahir akan hidup jika pola kematian saat ini tetap sama
9. Jumlah_fertiliti: Jumlah anak yang akan lahir dari setiap wanita jika tingkat kesuburan usia saat ini tetap sama
10. GDPperkapita: GDP per kapita. Dihitung sebagai Total GDP dibagi dengan total populasi.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

df = pd.read_csv("/content/Data_Negara_HELP (1).csv")
print("Shape dataset : ", df.shape)
print('\nInformasi dataset')
df.info()
print('\nStatistik deskriptif')
df.describe()

print('Lima data teratas')
df.head()

"""Dari 9 fitur, kita kelompokan menjadi 2 bagian yaitu 
1. bidang kesehatan : Kematian_anak, Kesehatan, Harapan_hidup dan Jumlah_fertiliti
2. bidang ekonomi : Ekspor, Impor, Pendapatan, Inflasi, GDPperkapita
"""

#Missing value
df.isnull().sum()

#Menghapus kolom Negara
df_olah = df.copy()
df_olah.drop(columns=["Negara"], inplace=True)
df_olah.head()

"""#Data Outlier"""

def remove_outlier(x):
  q1 = x.quantile(0.25)
  q3 = x.quantile(0.75)
  IQR = q3 - q1
  lower_bound = q1 - (IQR * 1.5)
  upper_bound = q3 + (IQR * 1.5)
  df_outlier = x[~((x < lower_bound) | (x > upper_bound))]
  return df_outlier

df_outlier = remove_outlier(df_olah)
df_outlier.fillna(method='ffill', inplace=True)
df_outlier.head()

df_outlier.isnull().sum()

"""#Korelasi antar fitur"""

plt.figure(figsize=(12,12))
sns.heatmap(df_outlier.corr(), annot=True)

"""Dua variabel dikatakan berkolerasi apabila perubahan pada variabel yang satu akan diikuti perubahan pada variabel yang lain secara teratur dengan arah yang sama (korelasi positif) atau berlawanan (korelasi negatif). Nilai korelasi berada pada rentang -1 sampai 0. Hubungan semakin kuat dengan arah yang sama jika korelasi bernilai mendekati angka 1, dan hubungan semakin kuat dengan arah yang berbeda jika korelasi bernilai mendekati angka -1. Jika korelasi berada disekitar angka 0, maka hubungan dinilai tidak begitu kuat (Tidak berpengaruh).

Kita dapat memilih pasangan fitur sesuai bidangnya masing-masing yang memiliki pengaruh kuat satu sama lain. (Korelasi bernilai lebih dari 0.6 atau kurang dari -0.6)

bidang kesehatan :    
1. Kematian_anak dan Jumlah_fertiliti (korelasi : 0.82)
2. Jumlah_fertiliti dan Harapan_hidup (korelasi : -0,8)
3. Harapan_hidup dan Kematian_anak (korelasi : -0,81)

bidang ekonomi :     
1. GDPperkapita dan Pendapatan (korelasi : 0.61)

Sedangkan untuk fitur yang berbeda bidang :    
1. Harapan_hidup dan Pendapatan (korelasi : 0.67)

#Kematian_anak dan Jumlah_fertiliti
"""

df_KJ = pd.DataFrame(data= df_outlier, columns=['Kematian_anak','Jumlah_fertiliti'])
df_KJ.head()

#Scalling data
sc = StandardScaler()
df_KJ = sc.fit_transform(df_KJ)

#Elbow Method Kematian_anak dan Jumlah_fertiliti
wcss = [] #Within-Cluster Sum of Square 
for i in range(1,11):
  kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
  kmeans.fit(df_KJ)
  wcss.append(kmeans.inertia_)

plt.figure(figsize=(10,6))
plt.plot(range(1,11), wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of cluster')
plt.ylabel('WCSS')
plt.show()

"""pada grafik diatas, kurva memiliki belokan yang tajam di titik 2, sehingga data ini akan dibuat dalam 2 cluster"""

#Silhoutte score untuk Kematian_anak dan Jumlah_fertiliti
from sklearn.metrics import silhouette_score

for i in range(2,11):
  labels = KMeans(n_clusters=i, init='k-means++', random_state=42).fit(df_KJ).labels_
  print("Silhoutte Score for " + str(i) + " cluster is " + str(silhouette_score(df_KJ, labels)))

"""Silhoutte score digunakan untuk melihat nilai k (banyaknya cluster) yang terbaik dilihat dari nilai yang tertinggi. Diperoleh Silhoutte score tertingginya yaiut 0.6607 untuk 2 cluster."""

#KMeans Cluster Kematian_anak dan Jumlah_fertiliti
#2 cluster
kmeans_KJ = KMeans(n_clusters=2, init='k-means++', random_state=42).fit(df_KJ)
labels_KJ = kmeans_KJ.labels_

df_KJ_cluster = pd.DataFrame(data= df_outlier, columns=['Kematian_anak','Jumlah_fertiliti'])
df_KJ_cluster['cluster'] = labels_KJ
df_KJ_cluster.head()

df_KJ_scal = pd.DataFrame(data= df_KJ, columns=['Kematian_anak','Jumlah_fertiliti'])
df_KJ_scal['cluster'] = labels_KJ
df_KJ_scal.head()

#Scatter Plot Kematian_anak dan Jumlah_fertiliti
plt.figure(figsize=(12,8))
print('n_cluster = 2')
plt.scatter(df_KJ_scal['Kematian_anak'][df_KJ_scal['cluster']==0], df_KJ_scal['Jumlah_fertiliti'][df_KJ_scal['cluster']==0], c='blue', s=100, edgecolors='black' )
plt.scatter(df_KJ_scal['Kematian_anak'][df_KJ_scal['cluster']==1], df_KJ_scal['Jumlah_fertiliti'][df_KJ_scal['cluster']==1], c='green', s=100, edgecolors='black' )

cluster = kmeans_KJ.cluster_centers_
plt.scatter(cluster[:,0], cluster[:,1], c='black', s=500)
plt.xlabel('Kematian_anak')
plt.ylabel('Jumlah_fertiliti')
plt.show()

"""Interpretasi :
Bisa dilihat bahwa terdapat 2 cluster. Cluster dengan label 1 berwarna hijau menunjukkan kecenderungan Kematian_anak dan jumlah_fertilitinya rendah, sedangkan cluster dengan label 0 berwarna biru menunjukkan kecenderungan Kematian_anak dan Jumlah_fertilitinya tinggi.
"""

df_KJ_cluster.groupby(['cluster']).agg({'Kematian_anak':'mean', 'Jumlah_fertiliti':'mean'})

"""Bisa disimpulkan:

cluster 0 : memiliki rata-rata tingkat kematian anak yang tinggi, yaitu 82 kematian anak per 1000 kelahiran dengan rata-rata 4 anak yang lahir dari setiap wanita

cluster 1 : memiliki rata-rata tingkat kematian anak yang rendah, yaitu 17 kematian anak per 1000 kelahiran dengan rata-rata 2 anak yang lahir dari setiap wanita
"""

cluster_KJ = pd.concat([df['Negara'],df_KJ_cluster], axis=1, join='outer')
cluster_KJ.head()

print('daftar negara cluster 0 :')
print(cluster_KJ[cluster_KJ.cluster == 0].Negara.values)
print('Total : ', cluster_KJ[cluster_KJ.cluster == 0].Negara.count())

print('daftar negara cluster 1 :')
print(cluster_KJ[cluster_KJ.cluster == 1].Negara.values)
print('Total : ', cluster_KJ[cluster_KJ.cluster == 1].Negara.count())

"""Dari hasil analisis diatas, negara yang ada di cluster 0 akan dipertimbangkan untuk menjadi penerima bantuan dari organisasi HELP dikarenakan tingginya tingkat kematian_anak dan juga jumlah_fertiliti

#Jumlah_fertiliti dan Harapan_hidup
"""

df_JH = pd.DataFrame(data= df_outlier, columns=['Jumlah_fertiliti','Harapan_hidup'])
df_JH.head()

#Scalling data
sc = StandardScaler()
df_JH = sc.fit_transform(df_JH)

#Elbow Method Jumlah_fertiliti dan Harapan_hidup
wcss = [] #Within-Cluster Sum of Square 
for i in range(1,11):
  kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
  kmeans.fit(df_JH)
  wcss.append(kmeans.inertia_)

plt.figure(figsize=(10,6))
plt.plot(range(1,11), wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of cluster')
plt.ylabel('WCSS')
plt.show()

"""pada grafik diatas, kurva memiliki belokan yang tajam di titik 2, sehingga data ini akan dibuat dalam 2 cluster"""

#Silhoutte score untuk Jumlah_fertiliti dan Harapan_hidup

for i in range(2,11):
  labels = KMeans(n_clusters=i, init='k-means++', random_state=42).fit(df_JH).labels_
  print("Silhoutte Score for " + str(i) + " cluster is " + str(silhouette_score(df_JH, labels)))

"""[link text](https://)Silhoutte score digunakan untuk melihat nilai k (banyaknya cluster) yang terbaik dilihat dari nilai yang tertinggi. Diperoleh Silhoutte score tertingginya yaiut 0.6196 untuk 2 cluster."""

#KMeans Cluster Jumlah_fertiliti dan Harapan_hidup
#2 cluster
kmeans_JH = KMeans(n_clusters=2, init='k-means++', random_state=42).fit(df_JH)
labels_JH = kmeans_JH.labels_

df_JH_cluster = pd.DataFrame(data= df_outlier, columns=['Jumlah_fertiliti', 'Harapan_hidup'])
df_JH_cluster['cluster'] = labels_JH
df_JH_cluster.head()

df_JH_scal = pd.DataFrame(data= df_JH, columns=['Jumlah_fertiliti','Harapan_hidup'])
df_JH_scal['cluster'] = labels_JH
df_JH_scal.head()

#Scatter Plot Jumlah_fertiliti dan Harapan_hidup
plt.figure(figsize=(12,8))
print('n_cluster = 2')
plt.scatter(df_JH_scal['Jumlah_fertiliti'][df_JH_scal['cluster']==0], df_JH_scal['Harapan_hidup'][df_JH_scal['cluster']==0], c='blue', s=100, edgecolors='black' )
plt.scatter(df_JH_scal['Jumlah_fertiliti'][df_JH_scal['cluster']==1], df_JH_scal['Harapan_hidup'][df_JH_scal['cluster']==1], c='green', s=100, edgecolors='black' )

cluster = kmeans_JH.cluster_centers_
plt.scatter(cluster[:,0], cluster[:,1], c='black', s=500)
plt.xlabel('Jumlah_fertiliti')
plt.ylabel('Harapan_hidup')
plt.show()

"""Interpretasi :
Bisa dilihat bahwa terdapat 2 cluster. Cluster dengan label 1 berwarna hijau menunjukkan kecenderungan Jumlah_fertilitinya tinggi namun Harapan_hidupnya rendah, sedangkan cluster dengan label 0 berwarna biru menunjukkan kecenderungan Jumlah_fertilitinya rendah namun Harapan_hidupnya tinggi
"""

df_JH_cluster.groupby(['cluster']).agg({'Jumlah_fertiliti':'mean','Harapan_hidup':'mean', })

"""Bisa disimpulkan:

cluster 0 : memiliki rata-rata Harapan hidup yang tinggi, yaitu 75 tahun. Kemudian jumlah fertilitinya 2, artinya rata-rata 2 anak lahir dari setiap wanita.

cluster 1 : memiliki rata-rata Harapan hidup lebih rendah dari cluster 0, yaitu 61 tahun. Kemudian jumlah fertilitinya 4, artinya rata-rata 4 anak lahir dari setiap wanita.
"""

cluster_JH = pd.concat([df['Negara'],df_JH_cluster], axis=1, join='outer')
cluster_JH.head()

print('daftar negara cluster 0 :')
print(cluster_JH[cluster_JH.cluster == 0].Negara.values)
print('Total : ', cluster_JH[cluster_JH.cluster == 0].Negara.count())

print('daftar negara cluster 1 :')
print(cluster_JH[cluster_JH.cluster == 1].Negara.values)
print('Total : ', cluster_JH[cluster_JH.cluster == 1].Negara.count())

"""Dari hasil analisis diatas, negara yang ada di cluster 1 akan dipertimbangkan untuk menjadi penerima bantuan dari organisasi HELP dikarenakan tingginya jumlah_fertiliti namun harapan hidupnya rendah.

#Harapan_hidup dan Kematian_anak
"""

df_HK = pd.DataFrame(data= df_outlier, columns=['Harapan_hidup', 'Kematian_anak'])
df_HK.head()

#Scalling data
sc = StandardScaler()
df_HK = sc.fit_transform(df_HK)

#Elbow Method Harapan_hidup dan Kematian_anak
wcss = [] #Within-Cluster Sum of Square 
for i in range(1,11):
  kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
  kmeans.fit(df_HK)
  wcss.append(kmeans.inertia_)

plt.figure(figsize=(10,6))
plt.plot(range(1,11), wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of cluster')
plt.ylabel('WCSS')
plt.show()

"""pada grafik diatas, kurva memiliki belokan yang tajam di titik 2, sehingga data ini akan dibuat dalam 2 cluster"""

#Silhoutte score untuk Harapan_hidup dan Kematian_anak

for i in range(2,11):
  labels = KMeans(n_clusters=i, init='k-means++', random_state=42).fit(df_HK).labels_
  print("Silhoutte Score for " + str(i) + " cluster is " + str(silhouette_score(df_HK, labels)))

"""Silhoutte score digunakan untuk melihat nilai k (banyaknya cluster) yang terbaik dilihat dari nilai yang tertinggi. Diperoleh Silhoutte score tertingginya yaiut 0.6160 untuk 2 cluster."""

#KMeans Cluster Harapan_hidup dan Kematian_anak
#2 cluster
kmeans_HK = KMeans(n_clusters=2, init='k-means++', random_state=42).fit(df_HK)
labels_HK = kmeans_HK.labels_

df_HK_cluster = pd.DataFrame(data= df_outlier, columns=['Harapan_hidup', 'Kematian_anak'])
df_HK_cluster['cluster'] = labels_HK
df_HK_cluster.head()

df_HK_scal = pd.DataFrame(data= df_HK, columns=['Harapan_hidup','Kematian_anak'])
df_HK_scal['cluster'] = labels_HK
df_HK_scal.head()

#Scatter Plot Harapan_hidup dan Kematian_anak
plt.figure(figsize=(12,8))
print('n_cluster = 2')
plt.scatter(df_HK_scal['Harapan_hidup'][df_HK_scal['cluster']==0], df_HK_scal['Kematian_anak'][df_HK_scal['cluster']==0], c='blue', s=100, edgecolors='black' )
plt.scatter(df_HK_scal['Harapan_hidup'][df_HK_scal['cluster']==1], df_HK_scal['Kematian_anak'][df_HK_scal['cluster']==1], c='green', s=100, edgecolors='black' )

cluster = kmeans_HK.cluster_centers_
plt.scatter(cluster[:,0], cluster[:,1], c='black', s=500)
plt.xlabel('Harapan_hidup')
plt.ylabel('Kematian_anak')
plt.show()

"""Interpretasi :
Bisa dilihat bahwa terdapat 2 cluster. Cluster dengan label 1 berwarna hijau menunjukkan kecenderungan Kematian_anak tinggi namun Harapan_hidupnya rendah, sedangkan cluster dengan label 0 berwarna biru menunjukkan kecenderungan Kematian_anak rendah namun Harapan_hidupnya tinggi
"""

df_HK_cluster.groupby(['cluster']).agg({'Harapan_hidup':'mean','Kematian_anak':'mean' })

"""Bisa disimpulkan:

cluster 0 : memiliki rata-rata Harapan hidup yang tinggi, yaitu 75 tahun dengan rata-rata terdapat 14 Kematian anak per 10000 kelahiran

cluster 1 : memiliki rata-rata Harapan hidup lebih rendah dari cluster 0, yaitu 61 tahun dengan rata-rata terdapat 76 Kematian anak per 10000 kelahiran
"""

cluster_HK = pd.concat([df['Negara'],df_HK_cluster], axis=1, join='outer')
cluster_HK.head()

print('daftar negara cluster 0 :')
print(cluster_HK[cluster_HK.cluster == 0].Negara.values)
print('Total : ', cluster_HK[cluster_HK.cluster == 0].Negara.count())

print('daftar negara cluster 1 :')
print(cluster_HK[cluster_HK.cluster == 1].Negara.values)
print('Total : ', cluster_HK[cluster_HK.cluster == 1].Negara.count())

"""Dari hasil analisis diatas, negara yang ada di cluster 1 akan dipertimbangkan untuk menjadi penerima bantuan dari organisasi HELP dikarenakan tingginya Kematian_anak namun harapan hidupnya rendah.

#GDPperkapita dan Pendapatan
"""

df_GP = pd.DataFrame(data= df_outlier, columns=['GDPperkapita', 'Pendapatan'])
df_GP.head()

#Scalling data
sc = StandardScaler()
df_GP = sc.fit_transform(df_GP)

#Elbow Method GDPperkapita dan Pendapatan
wcss = [] #Within-Cluster Sum of Square 
for i in range(1,11):
  kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
  kmeans.fit(df_GP)
  wcss.append(kmeans.inertia_)

plt.figure(figsize=(10,6))
plt.plot(range(1,11), wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of cluster')
plt.ylabel('WCSS')
plt.show()

"""pada grafik diatas, kurva memiliki belokan yang tajam di titik 2 dan titik 4, sehingga kita akan sesuaikan dengan Sillhoutte score untuk menentukan banyaknya cluster yang akan dibuat."""

#Silhoutte score untuk GDPperkapita dan Pendapatan

for i in range(2,11):
  labels = KMeans(n_clusters=i, init='k-means++', random_state=42).fit(df_GP).labels_
  print("Silhoutte Score for " + str(i) + " cluster is " + str(silhouette_score(df_GP, labels)))

"""Silhoutte score digunakan untuk melihat nilai k (banyaknya cluster) yang terbaik dilihat dari nilai yang tertinggi. Diperoleh Silhoutte score tertingginya yaiut 0.6298 untuk 4 cluster."""

#KMeans Cluster GDPperkapita dan Pendapatan
#4 cluster
kmeans_GP = KMeans(n_clusters=4, init='k-means++', random_state=42).fit(df_GP)
labels_GP = kmeans_GP.labels_

df_GP_cluster = pd.DataFrame(data= df_outlier, columns=['GDPperkapita', 'Pendapatan'])
df_GP_cluster['cluster'] = labels_GP
df_GP_cluster.head()

df_GP_scal = pd.DataFrame(data= df_GP, columns=['GDPperkapita','Pendapatan'])
df_GP_scal['cluster'] = labels_GP
df_GP_scal.head()

#Scatter Plot GDPperkapita dan Pendapatan
plt.figure(figsize=(12,8))
print('n_cluster = 4')
plt.scatter(df_GP_scal['GDPperkapita'][df_GP_scal['cluster']==0], df_GP_scal['Pendapatan'][df_GP_scal['cluster']==0], c='blue', s=100, edgecolors='black' )
plt.scatter(df_GP_scal['GDPperkapita'][df_GP_scal['cluster']==1], df_GP_scal['Pendapatan'][df_GP_scal['cluster']==1], c='green', s=100, edgecolors='black' )
plt.scatter(df_GP_scal['GDPperkapita'][df_GP_scal['cluster']==2], df_GP_scal['Pendapatan'][df_GP_scal['cluster']==2], c='red', s=100, edgecolors='black' )
plt.scatter(df_GP_scal['GDPperkapita'][df_GP_scal['cluster']==3], df_GP_scal['Pendapatan'][df_GP_scal['cluster']==3], c='yellow', s=100, edgecolors='black' )

cluster = kmeans_GP.cluster_centers_
plt.scatter(cluster[:,0], cluster[:,1], c='black', s=500)
plt.xlabel('GDPperkapita')
plt.ylabel('Pendapatan')
plt.show()

"""Interpretasi :
Bisa dilihat bahwa terdapat 4 cluster

cluster 0 (biru) :  Merupakan negara-negara yang memiliki pendapatan dan GDPperkapita menengah (tidak tinggi dan tidak juga rendah.

cluster 1 (hijau) :  Merupakan negara-negara yang memiliki pendapatan dan GDPperkapita tinggi.

cluster 2 (merah) :  Merupakan negara-negara yang memiliki pendapatan dan GDPperkapita rendah.

cluster 3 (kuning) :  Merupakan negara-negara yang memiliki pendapatan tinggi namun GDPperkapitanya rendah. Bisa dilihat bahwa pendapatan cluster ini bahkan rata-ratanya melebihi pendapatan cluster 1.
"""

df_GP_cluster.groupby(['cluster']).agg({'GDPperkapita':'mean','Pendapatan':'mean' })

"""Bisa disimpulkan:

cluster 0 : memiliki rata-rata GDPperkapita dan pendapatan yang tidak terlalu tinggi dan juga tidak terlalu rendah dibanding dengan negara lain.

cluster 1 : memiliki rata-rata GDPperkapita sangat tinggi yaitu 23835.29 dan juga rata-rata pendapatan tinggi yaitu $33141.17 per orang.

cluster 2 : memiliki rata-rata GDPperkapita sangat rendah, yaitu hanya 2170.34 dan juga rata-rata pendapatan yang sangat rendah yaitu hanya $4703.04 per orang.

cluster 3 : memiliki rata-rata GDPperkapita yang bisa dibilang rendah, tidak jauh dari cluster 2, yaitu hanya 4377.75 namun rata-rata pendapatan per orangnya sangatlah tinggi, bahkan lebih tinggi dari cluster 1, yaitu $40812.5.
"""

cluster_GP = pd.concat([df['Negara'],df_GP_cluster], axis=1, join='outer')
cluster_GP.head()

print('daftar negara cluster 0 :')
print(cluster_GP[cluster_GP.cluster == 0].Negara.values)
print('Total : ', cluster_GP[cluster_GP.cluster == 0].Negara.count())

print('daftar negara cluster 1 :')
print(cluster_GP[cluster_GP.cluster == 1].Negara.values)
print('Total : ', cluster_GP[cluster_GP.cluster == 1].Negara.count())

print('daftar negara cluster 2 :')
print(cluster_GP[cluster_GP.cluster == 2].Negara.values)
print('Total : ', cluster_GP[cluster_GP.cluster == 2].Negara.count())

print('daftar negara cluster 3 :')
print(cluster_GP[cluster_GP.cluster == 3].Negara.values)
print('Total : ', cluster_GP[cluster_GP.cluster == 3].Negara.count())

"""Dari hasil analisis diatas, negara yang ada di cluster 2 akan dipertimbangkan untuk menjadi penerima bantuan dari organisasi HELP dikarenakan GDPperkapita dan pendapatan sangatlah rendah dibandingkan dengan cluster-cluster yang lain."""



"""#Harapan_hidup dan Pendapatan"""

df_HP = pd.DataFrame(data= df_outlier, columns=['Harapan_hidup', 'Pendapatan'])
df_HP.head()

#Scalling data
sc = StandardScaler()
df_HP = sc.fit_transform(df_HP)

#Elbow Method Harapan_hidup dan Pendapatan
wcss = [] #Within-Cluster Sum of Square 
for i in range(1,11):
  kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
  kmeans.fit(df_HP)
  wcss.append(kmeans.inertia_)

plt.figure(figsize=(10,6))
plt.plot(range(1,11), wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of cluster')
plt.ylabel('WCSS')
plt.show()

"""pada grafik diatas, kurva memiliki belokan yang tajam di titik 2 dan titik 3, sehingga kita akan sesuaikan dengan Sillhoutte score untuk menentukan banyaknya cluster yang akan dibuat."""

#Silhoutte score untuk Harapan_hidup dan Pendapatan

for i in range(2,11):
  labels = KMeans(n_clusters=i, init='k-means++', random_state=42).fit(df_HP).labels_
  print("Silhoutte Score for " + str(i) + " cluster is " + str(silhouette_score(df_HP, labels)))

"""Silhoutte score digunakan untuk melihat nilai k (banyaknya cluster) yang terbaik dilihat dari nilai yang tertinggi. Diperoleh Silhoutte score tertingginya yaiut 0.52880 untuk 3 cluster."""

#KMeans Cluster Harapan_hidup dan Pendapatan
#3 cluster
kmeans_HP = KMeans(n_clusters=3, init='k-means++', random_state=42).fit(df_HP)
labels_HP = kmeans_HP.labels_

df_HP_cluster = pd.DataFrame(data= df_outlier, columns=['Harapan_hidup', 'Pendapatan'])
df_HP_cluster['cluster'] = labels_HP
df_HP_cluster.head()

df_HP_scal = pd.DataFrame(data= df_HP, columns=['Harapan_hidup','Pendapatan'])
df_HP_scal['cluster'] = labels_HP
df_HP_scal.head()

#Scatter Plot Harapan_hidup dan pendapatan
plt.figure(figsize=(12,8))
print('n_cluster = 3')
plt.scatter(df_HP_scal['Harapan_hidup'][df_HP_scal['cluster']==0], df_HP_scal['Pendapatan'][df_HP_scal['cluster']==0], c='blue', s=100, edgecolors='black' )
plt.scatter(df_HP_scal['Harapan_hidup'][df_HP_scal['cluster']==1], df_HP_scal['Pendapatan'][df_HP_scal['cluster']==1], c='green', s=100, edgecolors='black' )
plt.scatter(df_HP_scal['Harapan_hidup'][df_HP_scal['cluster']==2], df_HP_scal['Pendapatan'][df_HP_scal['cluster']==2], c='red', s=100, edgecolors='black' )


cluster = kmeans_HP.cluster_centers_
plt.scatter(cluster[:,0], cluster[:,1], c='black', s=500)
plt.xlabel('Harapan_hidup')
plt.ylabel('Pendapatan')
plt.show()

"""Interpretasi :
Bisa dilihat bahwa terdapat 3 cluster

cluster 0 (biru) :  Merupakan negara-negara yang memiliki pendapatan dan harapan hidup rendah

cluster 1 (hijau) :  Merupakan negara-negara yang memiliki pendapatan rendah namun harapan hidup cukup tinggi.

cluster 2 (merah) :  Merupakan negara-negara yang memiliki pendapatan dan harapan hidup yang sangat tinggi.

"""

df_HP_cluster.groupby(['cluster']).agg({'Harapan_hidup':'mean','Pendapatan':'mean' })

"""Bisa disimpulkan:

cluster 0 : memiliki rata-rata harapan hidup dan pendapatan sangat rendah, dengan rata-rata harapan hidup hanya 61 tahun dan pendapatan hanya $3923.61 per orang.

cluster 1 : memiliki rata-rata harapan hidup cukup tinggi namun dengan rata-rata pendapatan rendah. Rata-rata harapan hidupnya 74 tahun dengan pendapatan setiap orang $11895.16.

cluster 2 : memiliki rata-rata hidup dan pendapatan sangat tinggi, dengan rata-rata harapan hidup mencapai 79 tahun dan rata-rata pendapatan mencapai $37168.75 per orang.
"""

cluster_HP = pd.concat([df['Negara'],df_HP_cluster], axis=1, join='outer')
cluster_HP.head()

print('daftar negara cluster 0 :')
print(cluster_HP[cluster_HP.cluster == 0].Negara.values)
print('Total : ', cluster_HP[cluster_HP.cluster == 0].Negara.count())

print('daftar negara cluster 1 :')
print(cluster_HP[cluster_HP.cluster == 1].Negara.values)
print('Total : ', cluster_HP[cluster_HP.cluster == 1].Negara.count())

print('daftar negara cluster 2 :')
print(cluster_HP[cluster_HP.cluster == 2].Negara.values)
print('Total : ', cluster_HP[cluster_HP.cluster == 2].Negara.count())

"""Dari hasil analisis diatas, negara yang ada di cluster 0 akan dipertimbangkan untuk menjadi penerima bantuan dari organisasi HELP dikarenakan Harapan_hidup dan pendapatan cukup rendah.

#Analisis

Dilihat dari hasil clustering berdasarkan beberapa fitur yang memiliki korelasi yang tinggi, kita mendapatkan 1 cluster pada masing2 clustering untuk dipertimbangkan menjadi penerima bantuan dari organisasi HELP. Dari 5 clustering pasangan fitur, kita akan melihat negara mana yang ada pada setiap cluster yang dipertimbangka, sehingga kita dapat memilih negara tersebut sebagai negara yang paling tepat mendapatkan bantuan.

1. Kematian_anak dan Jumlah_fertiliti

pada clustering ini diperoleh cluster 0 menjadi pertimbangan untuk mendapatkan bantuan. Yaitu cluster dengan negara-negara yang memiliki tingkat Kematian_anak dan Jumlah_fertiliti tinggi.
"""

#Negara yang memiliki tingkat Kematian anak dan Jumlah fertiliti tinggi
NKJ = cluster_KJ[cluster_KJ.cluster == 0].Negara.values

print("Negara yang memiliki tingkat Kematian anak dan Jumlah fertiliti tinggi : " 
      + str(NKJ))
print("Banyaknya negara :" + str(len(NKJ)))

"""2. Jumlah_fertiliti dan Harapan_hidup

pada clustering ini diperoleh cluster 1 menjadi pertimbangan untuk mendapatkan bantuan. Yaitu cluster dengan negara-negara yang memiliki Jumlah_fertiliti tinggi namun Harapan_hidup rendah.
"""

#Negara yang memiliki Jumlah fertiliti tinggi dan Harapan_hidup rendah
NJH = cluster_JH[cluster_JH.cluster == 1].Negara.values

print("Negara yang memiliki Jumlah fertiliti tinggi dan Harapan_hidup rendah : " 
      + str(NJH))
print("Banyaknya negara :" + str(len(NJH)))

"""3. Harapan_hidup dan Kematian_anak

pada clustering ini diperoleh cluster 2 menjadi pertimbangan untuk mendapatkan bantuan. Yaitu cluster dengan negara-negara yang memiliki tingkat Kematian_anak tinggi namun Harapan_hidup rendah
"""

#Negara yang memiliki tingkat Kematian_anak tinggi dan Harapan_hidup rendah
NHK = cluster_HK[cluster_HK.cluster == 1].Negara.values

print("Negara yang memiliki tingkat Kematian_anak tinggi dan Harapan_hidup rendah : " 
      + str(NHK))
print("Banyaknya negara :" + str(len(NHK)))

"""4. GDPperkapita dan Pendapatan

pada clustering ini diperoleh cluster 2 menjadi pertimbangan untuk mendapatkan bantuan. Yaitu cluster dengan negara-negara yang memiliki GDPperkapitan dan Pendapatan sangat rendah.
"""

#Negara yang memiliki GDPperkapita dan Pendapatan rendah
NGP = cluster_GP[cluster_GP.cluster == 2].Negara.values

print("Negara yang memiliki GDPperkapita dan Pendapatan rendah : " 
      + str(NGP))
print("Banyaknya negara :" + str(len(NGP)))

"""5. Harapan_hidup dan Pendapatan

pada clustering ini diperoleh cluster 0 menjadi pertimbangan untuk mendapatkan bantuan. Yaitu cluster dengan negara-negara yang memiliki NHarapan_hidup dan Pendapatan rendah.
"""

#Negara yang memiliki Harapan_hidup dan Pendapatan rendah
NHP = cluster_HP[cluster_HP.cluster == 0].Negara.values

print("Negara yang memiliki Harapan_hidup dan Pendapatan rendah : " 
      + str(NHP))
print("Banyaknya negara :" + str(len(NHP)))

"""#Negara yang menerima bantuan

akan dicari negara yang masuk kedalam semua cluster yang menjadi pertimbangan, negara tersebut yang akan dipilih sebagai negara yang akan menerima bantuan dari organisasi HELP
"""

NB = list(set(NKJ.tolist()) & set(NJH.tolist()) & set(NHK.tolist()) & set(NGP.tolist()) & set(NHP.tolist()))

print("Negara yang dipilih untuk mendapatkan bantuan adalah : " + str(np.array(NB)))
print("Banyaknya Negara : " + str(len(NB))+ " Negara")

"""#Kesimpulan

Kesimpulannya, berdasarkan faktor sosial ekonomi dan kesehatan yang ada pada dataset, diperoleh dari hasil clustering bahwa ada 38 Negara yang memiliki kriteria sesuai dengan bantuan yang akan diberikan oleh organisasi HELP. 38 Negara tersebut disarankan untuk Negara-negara yang menjadi fokus CEO organisasi HELP sebagai Negara yang dianggap paling membutuhkan bantuan.
"""