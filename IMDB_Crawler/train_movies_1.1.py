from pickle import dump
from random import shuffle
from math import ceil

from elasticsearch.helpers import scan
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
import numpy as np

from settings import *

__version__ = '1.1'

# idx_lst = []
m_id_lst = []
m_plot_lst = []
m_genres_lst = []
genres_dict = {}

for _doc in scan(es, index=my_index, query={"query": {"match_all": {}}}):
	m_id_lst.append(_doc['_id'])
	m_plot_lst.append(_doc["_source"]["plots"])
	m_genres_lst.append(_doc["_source"]["genres"])

	g_m = []
	for _g in _doc["_source"]["genres"]:
		if _g not in genres_dict:
			genres_dict[_g] = len(genres_dict)
		g_m.append(genres_dict[_g])

genres_lst = sorted(genres_dict, key=genres_dict.get)

idx_lst = list(range(len(m_id_lst)))
shuffle(idx_lst)

X_train = np.array([m_plot_lst[i] for i in idx_lst[:ceil(len(idx_lst)*0.75)]])
y_train = [m_genres_lst[i] for i in idx_lst[:ceil(len(idx_lst)*0.75)]]
lb = MultiLabelBinarizer()
y_train = lb.fit_transform(y_train)

X_test = np.array([m_plot_lst[i] for i in idx_lst[ceil(len(idx_lst)*0.75):]])
y_test = [m_genres_lst[i] for i in idx_lst[ceil(len(idx_lst)*0.75):]]
m_id_test = [m_id_lst[i] for i in idx_lst[ceil(len(idx_lst)*0.75):]]

classifier = Pipeline([
	('vectorizer', CountVectorizer(stop_words='english', max_df=0.95, min_df=2)),
	('tfidf', TfidfTransformer()),
	('clf', OneVsRestClassifier(SVC(kernel='linear')))])

classifier.fit(X_train, y_train)
predicted = classifier.predict(X_test)
all_labels = lb.inverse_transform(predicted)

with open("classifier", "wb") as f:
	dump(classifier, f)
with open("X_test", "wb") as f:
	dump(X_test, f)
with open("y_test", "wb") as f:
	dump(y_test, f)
with open("all_labels", "wb") as f:
	dump(all_labels, f)
with open("m_id_test", "wb") as f:
	dump(m_id_test, f)

for movie, labels in zip(m_id_test, all_labels):
	print('{} => {}'.format(movie, ', '.join(x for x in labels)))

