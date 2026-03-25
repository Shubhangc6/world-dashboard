#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA


# All the libraries are installed

# In[2]:


df = pd.read_excel("World_development_mesurement.xlsx")
df.head()


# In[3]:


df.describe()


# In[4]:


df.info()


# In[5]:


df.isnull().sum()


# In[6]:


df.drop(['Business Tax Rate', 'Ease of Business', 'Hours to do Tax'], axis=1, inplace=True)


# Since there are columns which exceeds null values more than 40% they are dropped from the dataset

# In[7]:


cols = ['GDP', 'Health Exp/Capita', 'Tourism Inbound','Tourism Outbound'] 

for col in cols:
    df[col] = df[col].replace({'\$': '', '%': '', ',': ''}, regex=True)
    df[col] = pd.to_numeric(df[col], errors='coerce')


# Special symbols like $ % are removed from the data set and they are converted into numeric columns

# In[8]:


num_col = df.select_dtypes(include=['number'])
num_col = num_col.fillna(num_col.median())


# In[9]:


for col in num_col.columns:
    plt.figure(figsize=(6,3))
    sns.boxplot(x=num_col[col])
    plt.title(col)
    plt.show()


# Even though outliers are present in the dataset, they are retained because they represent real-world variations among countries. In the context of world development data, extreme values are meaningful (e.g., very high GDP or very low income countries) and contribute to better cluster differentiation. Removing them may lead to loss of important information.

# In[10]:


for col in num_col.columns:
    plt.figure(figsize=(6,3))
    sns.histplot(num_col[col], kde=True)
    plt.title(col)
    plt.show()


# Some features showed skewness due to economic inequality across countries, which is expected in world development data.

# In[11]:


corr = num_col.corr()

plt.figure(figsize=(12,8))
sns.heatmap(corr, cmap='coolwarm', annot=True, fmt=".2f",annot_kws={"size":8})
plt.title("Correlation Heatmap")
plt.show()


# In[12]:


corr_pairs = corr.abs().unstack().sort_values(ascending=False)
corr_pairs = corr_pairs[corr_pairs < 1].drop_duplicates()

top_pairs = corr_pairs.head(6).index.tolist()

for x_col, y_col in top_pairs:
    plt.figure(figsize=(6,4))
    sns.scatterplot(x=num_col[x_col], y=num_col[y_col])
    plt.title(f"{x_col} vs {y_col}")
    plt.show()


# In[13]:


#standardization
scaler = StandardScaler()
scaled_data = scaler.fit_transform(num_col)


# In[14]:


wcss = []

for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=42)
    kmeans.fit(scaled_data)
    wcss.append(kmeans.inertia_)

plt.plot(range(1,11), wcss, marker='o')
plt.title("Elbow Method")
plt.xlabel("No. of clusters")
plt.ylabel("WCSS")
plt.show()


# In[15]:


kmeans = KMeans(n_clusters=3, random_state=42)
kmeans_labels = kmeans.fit_predict(scaled_data)

dbscan = DBSCAN(eps=1.5, min_samples=5)
dbscan_labels = dbscan.fit_predict(scaled_data)

kmeans_score = silhouette_score(scaled_data, kmeans_labels)

if len(set(dbscan_labels)) > 1:
    dbscan_score = silhouette_score(scaled_data, dbscan_labels)
else:
    dbscan_score = -1

print("KMeans:", kmeans_score)
print("DBSCAN:", dbscan_score)


# In[16]:


pca = PCA(n_components=2)
pca_data = pca.fit_transform(scaled_data)


# In[17]:


plt.scatter(pca_data[:,0], pca_data[:,1], c=kmeans_labels)
plt.title("KMeans Clustering")
plt.show()


# In[18]:


plt.scatter(pca_data[:,0], pca_data[:,1], c=dbscan_labels)
plt.title("DBSCAN Clustering")
plt.show()


# In[19]:


df['Cluster'] = kmeans_labels
df.groupby('Cluster').mean(numeric_only=True)


# The dataset was cleaned by removing symbols, handling missing values, and dropping high-null columns. Exploratory data analysis was performed using boxplots, histograms, scatter plots, and correlation heatmaps. The data was standardized before applying clustering algorithms. KMeans and DBSCAN were implemented, and their performance was evaluated using silhouette score. KMeans performed better and was selected as the final model. PCA was used to visualize the clusters, and cluster-wise analysis provided meaningful insights into country groupings.

# In[ ]:





# In[ ]:




