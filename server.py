
from flask import Flask, request, render_template, jsonify
import json
import requests

app = Flask(__name__)

INDEX_NAME = "search-vault"


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/<data_type>/add", methods=["POST"])
def add_data(data_type):
    # Check for the data types we expect
    if request.method == "POST":
        data = request.get_data(as_text=True)
        r = requests.post('http://127.0.0.1:9200/'+INDEX_NAME+'/'+data_type + '/', data=data)
        json_response = r.json()
        return json_response["_id"]


@app.route("/<data_type>/search")
def search_data(data_type):
    # @TODO Check for the data types we expect
    # @TODO Do try catch outside request and handle gracefully using bootstrap
    if 'query' in request.args:
        r = requests.post('http://127.0.0.1:9200/'+INDEX_NAME+'/'+data_type + '/_search?q='+request.args['query'])
        response_dict = json.loads(r.text)
        return r.text
    else:
        # return a reasonable response
        return json.dumps(request.args)


if __name__ == "__main__":
    app.debug = True # only have this on for debugging!
    app.run(host='0.0.0.0') # need this to access from the outside world!
