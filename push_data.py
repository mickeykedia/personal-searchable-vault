__author__ = 'mayankkedia'

import urllib2

import requests

SERVER = "127.0.0.1"

r = requests.post("http://"+"SERVER"+":9200/_count", data='{"query":{ "match_all": {}}')
print r.json()

create_index = requests.get("http://"+"SERVER"+":9200/search-vault/")

data = """{
    "mappings": {
        "link":{
            "properties": {
                "link":{
                    "type":"string"
                },
                "comment":{
                    "type":"string",
                    "analyzer":"english"
                },
                "tags":{
                    "type":"string",
                    "analyzer":"english"
                },
                "created":  {
                    "type":   "date"
                }
            }
        },
        "movie":{
            "properties": {
                "name":{
                    "type":"string",
                    "analyzer":"english"
                },
                "year":{
                    "type":"date"
                },
                "comment":{
                    "type":"string",
                    "analyzer":"english"
                },
                "tags":{
                    "type":"string",
                    "analyzer":"english"
                },
                "created":  {
                    "type":   "date"
                }
            }
        },
        "book":{
            "properties": {
                "name":{
                    "type":"string",
                    "analyzer":"english"
                },
                "author":{
                    "type":"string"
                },
                "year":{
                    "type":"date"
                },
                "comment":{
                    "type":"string",
                    "analyzer":"english"
                },
                "tags":{
                    "type":"string",
                    "analyzer":"english"
                },
                 "created":  {
                    "type":   "date"
                }
            }
        },
        "place":{
            "properties": {
                "name":{
                    "type":"string",
                    "analyzer":"english"
                },
                "link":{
                    "type":"string"
                },
                "comment":{
                    "type":"string",
                    "analyzer":"english"
                },
                "tags":{
                    "type":"string",
                    "analyzer":"english"
                },
                "created":  {
                    "type":   "date"
                }
            }
        },
        "note":{
            "properties": {
                "note":{
                    "type":"string",
                    "analyzer":"english"
                },
                "comment":{
                    "type":"string",
                    "analyzer":"english"
                },
                "tags":{
                    "type":"string",
                    "analyzer":"english"
                },
                "created":  {
                    "type":   "date"
                }
            }
        },
        "idea":{
            "properties": {
                "name":{
                    "type":"string",
                    "analyzer":"english"
                },
                "idea":{
                    "type":"string",
                    "analyzer":"english"
                },
                "comment":{
                    "type":"string",
                    "analyzer":"english"
                },
                "tags":{
                    "type":"string",
                    "analyzer":"english"
                },
                 "created":  {
                    "type":   "date"
                }
            }
        }
    }
}"""
r = requests.post("http://"+"SERVER"+":9200/search-vault/", data=data)
print r.json()

link = '{"link":"https://github.com/scikit-learn/scikit-learn/pulls" , "comment":"This is the github page for contributing to the scikit learn library. Might be something useful to do, when you dont know what you want to do.", "tags":"things to do, scikit, machine learning, programming, github", "created":"2015-12-07"}'
add_link = requests.post("http://"+"SERVER"+":9200/search-vault/link/",data=link)
print add_link.json()

link = """{
            "link":"http://jsonlint.com",
            "comment":"A page for checking the veracity of jsons", 
            "tags":"NoSQL, JSON", 
            "created":"2015-12-07"
        }"""


add_link = requests.post("http://"+"SERVER"+":9200/search-vault/link/", data=link)
print add_link.json()

link = """{
            "link":"https://www.elastic.co/guide/en/elasticsearch/guide/current/_important_configuration_changes.html",
            "comment":"Configuration page for production deployment of elastic search", 
            "tags":"ElasticSearch, Search, production, deployment, elasticsearch.yaml", 
            "created":"2015-12-07"
        }"""
add_link = requests.post("http://"+"SERVER"+":9200/search-vault/link/", data=link)
print add_link.json()

note = """{
            "note":"USING PERIODIC COMMIT
            LOAD CSV WITH HEADERS FROM \"file:/Users/mayankkedia/Dropbox/Airbnb-Dropbox/network_evolution_data/network_evolution_2.csv\" AS row
            CREATE (:User {id_user_anon: row.id_user_anon, ds_account_created: row.ds_account_created, dim_market: row.dim_market, dim_age: row.dim_age, dim_gender: row.dim_gender, dim_network:2});",
            "comment":"Query on Neo4J for importing data as nodes from a csv", 
            "tags":"Neo4j, query, cypher, import data, csv, graph database", 
            "created":"2015-12-07"
        }"""
add_note = requests.post("http://"+"SERVER"+":9200/search-vault/note/", data=note)
print add_note.json()

link = """{
            "link":"http://elasticsearch.co",
            "comment":"Elastic search library page",
            "tags":"NoSQL, JSON, Elastic Search, indexing",
            "created":"2015-12-08"
        }"""
add_link = requests.post("http://"+"SERVER"+":500/link/add", data=link)
print add_link.json()

link = """{
            "link":"http://docs.python-requests.org/en/latest/",
            "comment":"Requests JSON library in python, documentation",
            "tags":"HTTP, requests, client, server, library, python",
            "created":"2015-12-08"
        }"""
add_link = requests.post("http://"+"SERVER"+":500/link/add", data=link)
print add_link.json()
