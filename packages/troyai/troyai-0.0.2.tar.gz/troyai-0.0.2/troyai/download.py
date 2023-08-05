import requests
import pickle

def download_model(url: str):
    request = requests.get(url)
    pickled_data = request.content
    return pickle.loads(pickled_data)