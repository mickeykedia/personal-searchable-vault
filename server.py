from flask import Flask, request, render_template, url_for
import json
import requests

app = Flask(__name__)

INDEX_NAME = "search-vault"

DATA_TYPE_DICT = dict(link=['tags', 'comment', 'link', 'created'],
                      note=['note', 'tags', 'comment', 'created'],
                      movie=['name', 'year', 'comment', 'tags', 'created'],
                      book=['name', 'author', 'year', 'comment', 'tags', 'created'],
                      place=['name', 'link', 'comment', 'tags', 'created'],
                      idea=['name', 'idea', 'comment', 'tags', 'created'])

ELASTIC_SERVER = '127.0.0.1:9200'


@app.route("/")
def home():
    """
    Route function for the homepage call.
    :return:
    """
    return render_template('index.html')


@app.route("/api/get")
def get_document_api():
    """
    API call for returning a particular document from the elastic search database
    :return: returns the response from the elastic search database as a string
    """
    if 'document_type' in request.args and 'document_id' in request.args:
        r = requests.get('http://' + ELASTIC_SERVER + '/' + INDEX_NAME + '/'
                         + request.args['document_type'] + '/' + request.args['document_id'])
    return r.text


def get_document(document_type, document_id):
    """
    Fetches a document from the elastic search database given the document_type and document_id
    :param document_type: Document type
    :param document_id: id of the document requested
    :return: json file with the response from the elastic search database
    """
    r = requests.get('http://' + ELASTIC_SERVER + '/' + INDEX_NAME + '/' + document_type + '/' + document_id)
    return r.json()


@app.route("/api/<document_type>/add", methods=["POST"])
def add_data_api(document_type):
    """
    API call for adding data. The data is expected to be in JSON format with
    the fields populated with values which have to be stored.
    :param document_type the document_type which the user wants to add
    :return: id of the indexed document
    """
    # Check for the data types we expect
    if request.method == "POST":
        data = request.get_data(as_text=True)
        return add_data_elastic_search_call(document_type, data=data)


def add_data_elastic_search_call(document_type, data):
    """
    Posts data to the elastic search server to add the data
    :param document_type: Document type to be added
    :param data: data to be added in the form of a json
    :return: returns the id of the added document
    """
    r = requests.post('http://' + ELASTIC_SERVER + '/' + INDEX_NAME + '/' + document_type + '/', data=data)
    json_response = r.json()
    if "_id" in json_response:
        return json_response["_id"]
    else:
        return "{}"


@app.route("/<document_type>/add", methods=["POST"])
def add_data(document_type):
    """
    Function to add data from form which has been 'posted' with relevant information
    :param document_type: Document type to be added
    :return: renders the index.html with a flag that data has been added
    """
    if request.method == "POST":
        data_dict = {}
        for d in DATA_TYPE_DICT[document_type]:
            if d in request.form and request.form[d]:
                data_dict[d] = request.form[d]
        return render_template('index.html',
                               add_res=get_document(document_type,
                                                    add_data_elastic_search_call(document_type, json.dumps(data_dict))))


def parse_search_result(response_dict):
    """
    Parses search results and returns the results
    :param response_dict:
    :return: Returns list of results or an empty list depending on response
    """
    if 'hits' in response_dict and response_dict['hits']['total'] > 0:
        results = response_dict['hits']['hits']
        return results
    else:
        # Return variable for setting a no result response
        return {}


@app.route("/api/search")
def search_data_api():
    """
    API call for searching data. API call expects atleast one argument in the GET request
    called 'query', an additional argument for 'document_type' can also be specified
    :return:
    """
    if 'query' in request.args:
        if 'document_type' in request.args:
            r = requests.post(
                'http://' + ELASTIC_SERVER + '/' + INDEX_NAME + '/' + request.args['document_type'] + '/_search?q=' +
                request.args['query'])
        else:
            r = requests.post('http://' + ELASTIC_SERVER + '/' + INDEX_NAME + '/_search?q=' + request.args['query'])
        response_dict = json.loads(r.text)
        return json.dumps(parse_search_result(response_dict))
    else:
        # return a reasonable response
        return json.dumps(request.args)


@app.route("/search")
def search_data():
    """
    Handles the search request from the web interface
    :return: Renders the search result
    """
    # @TODO Check for the data types we expect
    # @TODO Do try catch outside request and handle gracefully using bootstrap
    if 'query' in request.args:
        # calling the search api where the thread local request object is still available.
        return render_template('index.html', res=json.loads(search_data_api()))
    else:
        # return a reasonable response
        return json.dumps(request.args)


with app.test_request_context():
    print url_for("home")


if __name__ == "__main__":
    app.debug = True  # only have this on for debugging!
    app.run(host='0.0.0.0')  # need this to access from the outside world!
