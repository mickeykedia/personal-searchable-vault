from flask import Flask, request, render_template, jsonify
import json
import requests

app = Flask(__name__)

INDEX_NAME = "search-vault"

DATA_TYPE_DICT = dict(link=['tags', 'comment', 'link', 'created'], note=['note', 'tags', 'comment', 'created'],
                      movie=['name', 'year', 'comment', 'tags', 'created'],
                      book=['name', 'author', 'year', 'comment', 'tags', 'created'],
                      place=['name', 'link', 'comment', 'tags', 'created'],
                      idea=['name', 'idea', 'comment', 'tags', 'created'])

ELASTIC_SERVER = '127.0.0.1:9200'


@app.route("/")
def home():
    return render_template('index.html')


def get_document(data_type, document_id):
    r = requests.get('http://' + ELASTIC_SERVER + '/' + INDEX_NAME + '/' + data_type + '/' + document_id)
    return r.json()


@app.route("/api/<data_type>/add", methods=["POST"])
def add_data_api(data_type):
    # Check for the data types we expect
    if request.method == "POST":
        data = request.get_data(as_text=True)
        return add_data_elastic_search_call(data_type, data=data)


def add_data_elastic_search_call(data_type, data):
    r = requests.post('http://' + ELASTIC_SERVER + '/' + INDEX_NAME + '/' + data_type + '/', data=data)
    json_response = r.json()
    return json_response["_id"]


@app.route("/<data_type>/add", methods=["POST"])
def add_data(data_type):
    if request.method == "POST":
        data_dict = {}
        for d in DATA_TYPE_DICT[data_type]:
            if d in request.form and request.form[d]:
                data_dict[d] = request.form[d]
        #return json.dumps(get_document(data_type, add_data_elastic_search_call(data_type, json.dumps(data_dict))))
        return render_template('index.html', add_res=get_document(data_type, add_data_elastic_search_call(data_type, json.dumps(data_dict))))


def parse_search_result(response_dict):
    """

    :param response_dict:
    :return:
    """
    if 'hits' in response_dict and response_dict['hits']['total'] > 0:
        results = response_dict['hits']['hits']
        return results
    else:
        # Return variable for setting a no result response
        return {}


@app.route("/api/search")
def search_data_api():
    if 'query' in request.args:
        if 'data_type' in request.args:
            r = requests.post(
                'http://' + ELASTIC_SERVER + '/' + INDEX_NAME + '/' + request.args['data_type'] + '/_search?q=' +
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
    # @TODO Check for the data types we expect
    # @TODO Do try catch outside request and handle gracefully using bootstrap
    if 'query' in request.args:
        # calling the search api where the thread local request object is still available.
        return render_template('index.html', res=json.loads(search_data_api()))
    else:
        # return a reasonable response
        return json.dumps(request.args)


if __name__ == "__main__":
    app.debug = True  # only have this on for debugging!
    app.run(host='0.0.0.0')  # need this to access from the outside world!
