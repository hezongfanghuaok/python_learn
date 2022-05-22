import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
#%matplotlib inlinep

# 数据准备
data = make_blobs(n_samples=2000, centers=[[1,1], [-1, -1]], cluster_std=0.7, random_state=2018)
X = data[0]
y = data[1]

#设置聚类数量
n_clusters = 2

# 建立聚类模型对象
kmeans = KMeans(n_clusters=n_clusters, random_state=2018)
# 训练聚类模型
kmeans.fit(X)

# 预测聚类模型
pre_y = kmeans.predict(X)

### 模型效果指标评估 ###
# 样本距离最近的聚类中心的总和
inertias = kmeans.inertia_

# 调整后的兰德指数
adjusted_rand_s = metrics.adjusted_rand_score(y, pre_y)

# 互信息
mutual_info_s = metrics.mutual_info_score(y, pre_y)

# 调整后的互信息
adjusted_mutual_info_s = metrics.adjusted_mutual_info_score(y, pre_y)

# 同质化得分
homogeneity_s = metrics.homogeneity_score(y, pre_y)

# 完整性得分
completeness_s = metrics.completeness_score(y, pre_y)

# V-measure得分
v_measure_s = metrics.v_measure_score(y, pre_y)

# 平均轮廓系数
silhouette_s = metrics.silhouette_score(X, pre_y, metric='euclidean')

# Calinski 和 Harabaz 得分 不一样的库 有的是calinski_harabaz_score 有的是 calinski_harabasz_score
calinski_harabaz_s = metrics.calinski_harabaz_score(X, pre_y)


df_metrics = pd.DataFrame([[inertias, adjusted_rand_s,mutual_info_s, adjusted_mutual_info_s, homogeneity_s,completeness_s,v_measure_s, silhouette_s ,calinski_harabaz_s]],
                         columns=['ine','tARI','tMI','tAMI','thomo','tcomp','tv_m','tsilh','tc&h'])

df_metrics
## 模型可视化##
centers = kmeans.cluster_centers_
# 颜色设置
colors = ['green', 'pink']
# 创建画布
plt.figure(figsize=(12,6))
titles = ['Real', 'Predict']
for j, y_ in enumerate([y, pre_y]):
    plt.subplot(1,2, j+1)
    plt.title(titles[j])
    # 循环读类别
    for i in range(n_clusters):
        # 找到相同的索引
        index_sets = np.where(y_ == i)
        # 将相同类的数据划分为一个聚类子集
        cluster = X[index_sets]
        # 展示样本点
        plt.scatter(cluster[:, 0], cluster[:, 1], c=colors[i], marker='.')
        if j==1:
        # 簇中心
            plt.plot(centers[i][0], centers[i][1], 'o',markerfacecolor=colors[i],markeredgecolor='k', markersize=6)
plt.savefig('xx.png')
plt.show()

