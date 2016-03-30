from __future__ import print_function  # Use print() instead of print
from flask import url_for
from app import db
from app.models.collections import Collection 


def test_page_urls(client):

	# Login
	response = client.post(url_for('user.login'), follow_redirects=True,
						   data=dict(email='jeremy@incdb.com', password='Password1'))

	# Visit contribute page
	response = client.get(url_for('contribute.new_collection'))
	assert b'<h1>New Collection</h1>' in response.data

	# Create new collection with both Collection Name and Movie Name
	
	response = client.post(url_for('contribute.new_collection'), follow_redirects=True,
						   data=dict(name='collection_test_1', movie_name='movie_1'))
	print(db.session.query(Collection.name).all())
	collection = Collection.query.filter(Collection.movie_name=='movie_1').first()
	assert collection.movie_name == 'movie_1'
	#response = client.get(url_for('contribute.upload_files', collection='collection_test_1'))
	#assert b'<h1>Upload your data</h1>' in response.data
	

	# Try New collection with only collection name
	response = client.post(url_for('contribute.new_collection'), follow_redirects=True,
						   data=dict(name='collection_test_2', user_id='1'))
	assert b'<h1>New Collection</h1>' in response.data
	assert b'<span style="margin-top: 5px;" class="help-block">Movie Name is required.</span>' in response.data

	# Try new collection with only movie name
	response = client.post(url_for('contribute.new_collection'), follow_redirects=True,
						   data=dict(movie_name='movie_2', user_id='1'))
	assert b'<h1>New Collection</h1>' in response.data
	assert b'<span style="margin-top: 5px;" class="help-block">Name for collection is required.</span>' in response.data

	# Try new collection with none of required fields
	response = client.post(url_for('contribute.new_collection'), follow_redirects=True,
						   data=dict())
	assert b'<h1>New Collection</h1>' in response.data
	assert b'<span style="margin-top: 5px;" class="help-block">Name for collection is required.</span>' in response.data
	assert b'<span style="margin-top: 5px;" class="help-block">Movie Name is required.</span>' in response.data

	# Try new collection with existing colleciton name

	# Create new collection with existing movie name
	"""
	response = client.post(url_for('contribute.new_collection'), follow_redirects=True,
						   data=dict(name='collection_test_4', movie_name='movie_1', user_id='1'))
	response = client.get(url_for('contribute.upload_files', collection='collection_test_4'))
	assert b'<h1>Upload your data</h1>' in response.data
	"""

   
