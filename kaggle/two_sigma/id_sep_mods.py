import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
from sklearn import ensemble, linear_model
from collections import Counter

import time
from functools import wraps
from memory_profiler import profile
 
 
############# decorator function of time ######################
def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print ("Total time running %s: %s seconds" %
               (function.func_name, str(t1-t0))
               )
        return result
    return function_timer
############# decorator function of time ######################
@profile
def essentials():
	train = pd.read_hdf('../kaggle_data/train.h5')

	id_all = train.id
	id_count = Counter(id_all)
	ids_similar = map(lambda y: y[0], filter(lambda x:x[1]==1813, id_count.most_common(10000)))
	ids_similar_value = 1813 ## no of rows in all similar retrieved values.

	ids_un = train.id.unique()
	ids_sorted = sorted(ids_un)
	least_id = ids_sorted[-1]
	model_dict = {}

	important_features = ['technical_20', 'technical_30']
	data = train[important_features]
	data_mean = data.mean(axis = 0)
	data.fillna(data_mean, inplace=True)

	for i in important_features:
		data[i+'diff'] = data[i] - data[i].shift(1)
		important_features.append(i+'diff')
	
# cols_train = ['technical_20', 'technical_30', ]
class Features:

	def __init__(self, ids_similar):
		self.ids_similar = ids_similar

	def fit(self, x, y):
		model = linear_model.LinearRegression()
		model.fit(x, y)
		self.model = model

	def predict(self, x):
		return self.model.predict(x)

essentials()
# a = Features(ids_similar)
# print(a)