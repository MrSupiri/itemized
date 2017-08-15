import urllib.request
import os
import configparser
import json
import re
import shutil
import pickle


def getdata(data):
	os.chdir(os.path.dirname(os.path.abspath(__file__)))
	config = configparser.ConfigParser()
	config.read('data/config.ini')
	return config['config'][data]

def request(requesturl):
	source = urllib.request.urlopen(requesturl)
	data = json.loads(source.read().decode())
	return data

def getcurrentpatch():
	data = request('http://api.champion.gg/v2/champions?champData=patch&limit=1&api_key='+getdata('championgg_apikey'))
	return data[0]['patch']

def getchampname(id):
	return champions['data'][str(id)]['name'], champions['data'][str(id)]['title'].title()

def clear(s):
	return re.sub('[^A-Za-z0-9]+', '', s)

#champions = pickle.load(open('data\championlist.dat','rb'))

champions = request("https://euw1.api.riotgames.com/lol/static-data/v3/champions?locale=en_US&dataById=true&api_key="+getdata('riot_apikey'))
pickle.dump(champions,open('data\championlist.dat','wb'))


