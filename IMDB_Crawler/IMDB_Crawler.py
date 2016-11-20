from pickle import load

from elasticsearch import Elasticsearch
from imdbpie import Imdb
from pickle import dump

from es_method import load_to_elasticsearch, create_dataset, check_doc_exists

imdb = Imdb(anonymize=True) # to proxy requests

# Creating an instance with caching enabled
# Note that the cached responses expire every 2 hours or so.
# The API response itself dictates the expiry time)
# imdb = Imdb(cache=True)

# res = imdb.search_for_title("The Dark Knight")
# for _ in res:
# 	print(_)

with open("imdb_id_set", "rb") as f:
	imdb_id_set = load(f)

es = Elasticsearch()
my_index = "imdb_movies_index"
my_type = "movies"

# create_dataset(es, my_index, my_type)
failed_id_set = set()

for movie_id in imdb_id_set:
	# movie_id = "tt2112152"
	if not es.exists(index=my_index,
					   doc_type=my_type,
					   id=movie_id):

		if imdb.title_exists(movie_id):
			title_obj = imdb.get_title_by_id(movie_id)
		else:
			print("{} failed".format(movie_id))
			failed_id_set.add(movie_id)
			continue
		# print(title_obj)

		if title_obj:

			print(movie_id)
			m_title = title_obj.title if title_obj.title else ""
			m_genres = title_obj.genres if title_obj.genres else []
			m_plot_outline = title_obj.plot_outline if title_obj.plot_outline else ""
			m_plots = ' '.join(title_obj.plots) if title_obj.plots else ""
			m_year = title_obj.year if title_obj.year else 0
			m_type = title_obj.type if title_obj.type else ""
			m_rating = title_obj.rating if title_obj.rating else 0.0
			m_runtime = title_obj.runtime if title_obj.runtime else 0
			m_release_date = title_obj.release_date if title_obj.release_date else ""
			# m_credits = title_obj.credits if title_obj.credits else ""

			source = {
				"title": m_title,
				"year": m_year,
				"genres": m_genres,
				"plot_outline": m_plot_outline,
				'plots': m_plots,
				"type": m_type,
				"rating": m_rating,
				"runtime": m_runtime,
				"release_date": m_release_date
			}
			# print(source)
			# exit(-1)

			load_to_elasticsearch(es, my_index, my_type, source, movie_id)


	else:
		print("{} exists".format(movie_id))

with open("failed_id_set", "wb") as f:
	dump(failed_id_set, f)

