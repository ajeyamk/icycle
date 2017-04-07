
# data munging

import pandas as pd
import json

# clustering

from sklearn.cluster import KMeans
import numpy as np
import pickle


# get customer data

all_customers = pickle.load( open( "/home/ubuntu/all_customers.pkl", "rb" ) )

# util method top get zip of customers from their address

def mk_int(s):
    try:
        s = s.split('-')[0]
        try:
            int(s)
            return int(s) if s else 0
        except:
            return 0
    except:
        return 0

all_cust_zip = [{'id':cust['id'],'zip':mk_int(cust['addresses'][0]['zip'])} if len(cust['addresses']) > 0 else {'id':cust['id'],'zip':0} for cust in all_customers]


# In[66]:

# make clusters on customers based on geography

X = np.array([[0,cust_zip['zip']] for cust_zip in all_cust_zip])
kmeans = KMeans(n_clusters=20, random_state=0).fit(X)
cust_clust = [{'cust_id':cust_zip['id'],'cluster':kmeans.labels_[idx]} for idx,cust_zip in enumerate(all_cust_zip)]
cust_clust_df = pd.DataFrame(cust_clust)


# In[82]:

# getting some sample orders for checking processing
# data produced in this block is a Dataframe with 2 columns: ['cust_id','item_id']

with open('mult_orders.json', 'r') as jsonFile:
    all_orders = json.load(jsonFile)
user_item = list()
for order in all_orders:
    cust_id = order['customer']['id']
    for order_line_item in order['line_items']:
        prod_id = order_line_item['product_id']
        user_item = user_item + [(cust_id,prod_id)]

user_item = np.array(user_item)
user_item = pd.DataFrame(user_item)
user_item.columns = ['cust_id','item_id']


# In[107]:

# get cluster number for items by mapping items first to user and then to cluster

user_item_cluster = pd.merge(cust_clust_df, user_item, how='left', on=['cust_id'])


# In[111]:

# util method

def count_rows(df):
    df.shape[0]
    return df.shape[0]


# In[ ]:

# aggregating data

grouped = user_item_cluster.groupby(['cluster','item_id'])
result = grouped.agg(count_rows)
result = result.reset_index(level=['cluster','item_id'])
result.columns = ['cluster','item_id','order_count']


# In[161]:

# getting top 5 itemd in every cluster

item_clusters = list()
for name,group in result.groupby('cluster'):
    df = pd.DataFrame()
    df = group
    arr = np.array(df['order_count'])
    arr = arr.argsort()[-5:][::-1]
    items = np.array(df['item_id'][arr])
    item_cluster = {'cluster':int(df['cluster'][:1]),'items':items}
    item_clusters = item_clusters + [item_cluster]


# In[164]:

#forming the final dict:{'cust_id': 4993496844, 'recommended_items': []}

custs_items_recom = list()
for cust in cust_clust:
    recom_items = list()
    try:
        for item_cluster in item_clusters:
            if item_cluster['cluster']==cust['cluster']:
                recom_items = item_cluster['items']
                break
    except:
        pass
    cust_items_recom = {'cust_id':cust['cust_id'],'recommended_items':recom_items}
    custs_items_recom = custs_items_recom + [cust_items_recom]

