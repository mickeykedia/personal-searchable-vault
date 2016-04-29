# Personal-Searchable-Vault

A python flask based app with a backend in Elastic Search. The webapp defines different types of items that 
can be stored within the app and searched for using basic text search. 

# Motivation
The idea is that I come across so many things every day that I want to remember and tag in my own way, but I have no real searchable database for myself. This is a simple app which can do that. 

# Types of Items

- Link
- Movie
- Book 
- Place
- Note
- Idea

Each of these in turn has comments, tags etc. 

# How to setup 

## Setup Elastic Search 

This app works if the Elastic Search instance is also on the same server as the flask app. The Elastic Search application can be downloaded from [here](https://www.elastic.co/products/elasticsearch) and a single core instance can be run using 

`./elasticsearch-2.1.0/bin/elasticsearch -d -p pid` 

This will write the pid of the elastic search instance to a file called pid, which can then be used to kill the instance (when needed)

Note: Running Elastic Search on a cluster is not very complicated and they have very good documentation (seriously). Would suggest reading through it if looking to scale the system. 

## Configure Elastic Search

A very simple configuration works for the Elastic Search (ES) instance running on your local machine. For ES to work with the items you want to create an index (similar to Db) for these items (called 'Mappings') and their properties specifying the kind of indexing you want for each property. Again ES has great documentation, but the required mapping and index has been created in the file called `setup.py`

Running setup.py will do a post request to the local instance of ES and setup the required index (database) and mappings (tables). 

# To do 

### Partial text matching
The search functionality implemented doesn't do free text search yet. It searches for whole words but doesn't do partial matches. The reason for this are queries defined within the flask app (these are queries made to the ES instance). It is pretty simple to change that. 

### Security
Some sort of security layer must be introduced to make sure this can only be used by me
