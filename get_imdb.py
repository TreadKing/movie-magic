import requests
import os
import json
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

BASE_URL = "https://imdb-api.com/en/API"
API_KEY = os.getenv("API_KEY")

def get_name():
    r = requests.get(BASE_URL + "/SearchName/" + API_KEY + "/Jean Reno")
    r = r.json()
    #print(json.dumps(r, indent=4))
    #print(r["results"][0]["id"])
    actor_id = r["results"][0]["id"]
    search_name(actor_id)

def search_name(actor_id):
    r = requests.get(BASE_URL + "/Name/" + API_KEY + "/" +actor_id)
    r = r.json()
    for i in range(10):
        print(r["castMovies"][i]["title"])

get_name()