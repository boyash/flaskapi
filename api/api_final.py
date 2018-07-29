import flask #importing flask module
from flask import request, jsonify #from the flask module we are importing request and jsonify sub modules
import sqlite3 #we are importing sqlite 3 which will be used in the db further in the code

app = flask.Flask(__name__) #initialising the app
app.config["DEBUG"] = True #setting app config for debug to true to trace the issues during dev. Set it to false for production

def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

@app.route('/', methods=['GET']) #defining the root route of the app 
def home(): #this func returns a html string which is displayed in the browser when we hit localhost:5000 and acts as the root route of the app
	return '''<h1>Distant Reading Archive</h1> 
<p>A prototype API for Advanced reading of Data.</p>''' #replace it with a template 


@app.route('/api/v1/resources/books/all', methods=['GET']) #this is the api route url to fetch all the books from the sqlite3 db
def api_all(): 
	conn = sqlite3.connect('books.db')
	conn.row_factory = dict_factory
	cur = conn.cursor()
	all_books = cur.execute('SELECT * FROM books;').fetchall()

	return jsonify(all_books)

@app.errorhandler(404)
def page_not_found(e):
	return "<h1>404</h1><p>The resource could not be found.</p>",404


@app.route('/api/v1/resources/books', methods=['GET'])
def api_filter():
	query_parameters = request.args

	id= query_parameters.get('id')
	published = query_parameters.get('published')
	author = query_parameters.get('author')

	query = "SELECT * FROM books WHERE"
	to_filter = []


	if id:
		query += ' id=? AND'
		to_filter.append(id)
	if published:
		query += ' published=? AND'
		to_filter.append(published)
	if author:
	 	query += ' author=? AND'
	 	to_filter.append(author)
	if not(id or published or author):
	 	return page_not_found(404)

	query = query[:-4] + ';'
	conn = sqlite3.connect('books.db')
	conn.row_factory = dict_factory
	cur = conn.cursor()
	results = cur.execute(query, to_filter).fetchall()

	return jsonify(results)

app.run()

