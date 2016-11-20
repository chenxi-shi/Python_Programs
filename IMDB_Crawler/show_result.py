from pickle import load
import numpy as np

from es_method import search_doc
from settings import *

def hamming_loss_2(truth_lst, pred_lst):
	truth_set = set(truth_lst)
	pred_set = set(pred_lst)
	code_word_set = truth_set.union(pred_set)

	loss_score = len(code_word_set)

	for _c in code_word_set:
		in_truth = _c in truth_set
		in_pred = _c in pred_set
		if in_truth == in_pred:
			loss_score -= 1

	return loss_score

def hamming_loss(truth_lst, pred_lst):
	truth_set = set(truth_lst)
	pred_set = set(pred_lst)
	code_word_set = truth_set.union(pred_set)
	intersection_set = truth_set.intersection(pred_set)
	loss_score = len(code_word_set) - len(intersection_set)

	return loss_score

def get_accuracy(truth_lst, pred_lst):
	truth_set = set(truth_lst)
	pred_set = set(pred_lst)

	if truth_set == pred_set:
		return 1
	else:
		return 0

def jaccard_idx(truth_lst, pred_lst):
	truth_set = set(truth_lst)
	pred_set = set(pred_lst)
	code_word_set = truth_set.union(pred_set)
	intersection_set = truth_set.intersection(pred_set)

	return len(intersection_set) / len(code_word_set)

def jaccard_fi(truth_lst, pred_lst):
	truth_set = set(truth_lst)
	pred_set = set(pred_lst)
	intersection_set = truth_set.intersection(pred_set)

	return len(intersection_set) / (len(truth_set) + len(pred_set))


# with open("classifier", "rb") as f:
# 	classifier = load(f)
# with open("y_test", "rb") as f:
# 	y_test = load(f)
with open("all_labels", "rb") as f:
	all_labels = load(f)
with open("m_id_test", "rb") as f:
	m_id_test = load(f)

# m_plot_lst = []
m_genres_lst = []

for _doc in m_id_test:
	res = search_doc(es, my_index, my_type, {"_id":_doc})
	# m_plot_lst.append(res["_source"]["plots"])
	m_genres_lst.append(res["_source"]["genres"])


tt_test_movies = len(all_labels)
hamming_loss_score = 0
accuracy_score = 0
jaccard_idx_score = 0
jaccard_fi_score = 0
for i in range(tt_test_movies):
	print(m_genres_lst[i], all_labels[i])
	if not m_genres_lst[i] and not all_labels[i]:
		hamming_loss_score = accuracy_score = jaccard_idx_score = jaccard_fi_score = 1
	else:
		hamming_loss_score += hamming_loss(m_genres_lst[i], all_labels[i])
		accuracy_score += get_accuracy(m_genres_lst[i], all_labels[i])
		jaccard_idx_score += jaccard_idx(m_genres_lst[i], all_labels[i])
		jaccard_fi_score += jaccard_fi(m_genres_lst[i], all_labels[i])


print(hamming_loss_score/tt_test_movies)
print(accuracy_score/tt_test_movies)
print(jaccard_idx_score/tt_test_movies)
print(jaccard_fi_score/tt_test_movies)


# truth = [1,2,3]
# pred = [1,2,4,5]
# print(jaccard_idx(truth, pred))
# print(jaccard_fi(truth, pred))