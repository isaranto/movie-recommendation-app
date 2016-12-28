# MovieRama - Movie Recommendation app
![Alt text](/img/movierama.png?raw=true "MovieRama")

Instructions:
In order to run the flask app download the data (ratings and movie info) from [my Dropbox](https://www.dropbox.com/s/dsyxu59ax3qi3eb/movierama-data.zip?dl=0) and run homepage.py. Also you will need to provide the API key and app directory in the movierama/athenticate.py file.
This is a movie recommendation system using a collaborative filtering approach. I decided to use item-item collaborative filtering due to the fact that in the working prototype there is no specific user that has logged in, hence the proposed engine is not personilised. This way an item is recommended because users that liked the movie shown also liked the recommended one. This way there is a universal list of recommendations for each movie. After creating the user-item matrix. we create the item-item matrix which is being used for our predictions taking into account only the users who have rated the specified movie.

Alternative approaches:

	a)The alternative approach would be to use user-item collaborative filtering to achieve better,
	personalised results. In that case the recommendation would be in the form "users who are similar
	to you also liked". The	difference is that this way, the recommended items below each movie would
	be different for each user.	
	b)A more advanced method would be to deal with the matrix completion problem by decomposing the 
	user-item matrix in an SVD style approach, thus extracting the missing values (the predictions). 
	I have started the implementation of the algorithm using a least-squares solution for the cost function that
	calculates the error between the approximation user-item matrix (the product of the two factors UxV) and the
	original user-item matrix but it is not finished yet.

The script download.py serves the purpose of generating a dataset. We download movie info from MovieDB and save them into a json file. I have downloaded the movies with ids 1-10000 (5207 in total). Afterwards we randomly generate 200000 ratings from 1000 users.

The recommendation engine is in the Recommendation.py file.
Due to the fact that the matrix product is slow to calculate even for sparse matrices we are caching the predictions matrix using numpy's save function which pickles the result (./cache/recommendations/prediction.npy). Afterwards we can install a script which will be ran as a background service on the server running the engine which will call the clear_cache() and make_predictions() methods at specified periods during the day/week which will clear all caches on the server (searches, recommendations etc) and will compute the new predictions. The clear cache method will delete every cache file which is older than a week. If it is given the parameter all=True it will delete every cache, regardless its creating date.


In the given application the front and the backend systems communicate via the API which is in the form:
	1. The front end provides a query
	2. the backend system returns a json list. Each item in the list represents a movie (in the form of json entry- python dictionary) which also holds 5 recommendations (title, url) for each entry.

Things not implemented :

	1. At the moment the bottleneck of the application is the lack of the database. In the case where
	a query is not	retrieved from cache it takes too long because data are being retrieved from 
	files (movies,titles etc). I tried using the API but it cannot be used for such a prpose due to the
	request limit (40 requests every 10 seconds per	IP). All data should be saved in a database (relational or NOSQL)
	which will be used to query and extract	information about movies (search etc). Elasticsearch would be a very
	good choice, especially because it includes Lucene	which is also useful for a search engine. At the moment we
	are just saving in pickle format the dictionary	with the movies.

 	2. The first substantial improvement would be the personilised recommendations. Adding a login page
	in the front end and user-item filtering in the backend.

 	3. The movie page: at the moment clicking on a recommendation just navigates to the MovieDB page.
 	
 	4. Deal with the cold start problem: In the case where a movie has not been rated we could follow 
	the following approach: provide recommendations based on the text similarity of the movie desciption
 	combined with the genres it belongs to and give the recommendations sorted by average rating in 
 	descreasing order.
