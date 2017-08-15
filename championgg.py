import itemset
import json
import os
from tqdm import tqdm
import time
def deleteold(name,lane):
	path = itemset.getdata('lolpath') + "\config\Champions\{}\Recommended".format(name)
	files = os.listdir(path)

	for file in files:
		if lane in file.split('-'):
			file = os.path.join(path,file)
			print(file)
			os.remove(file)

def formatitems(arrays):
	temp = []
	for array in arrays:
		temp.append({"count": 1, "id": array})
	return temp

def builditeamset(elo):
	if itemset.getcurrentpatch() != itemset.getdata('lastpatch'):
		if elo:
			championsdata = itemset.request('http://api.champion.gg/v2/champions?elo='+elo+'&champData=hashes&api_key='+itemset.getdata('championgg_apikey'))
		else:
			championsdata = itemset.request(
				'http://api.champion.gg/v2/champions?champData=hashes&api_key=' + itemset.getdata(
					'championgg_apikey'))
		for championdata in championsdata:
			os.chdir(str(itemset.getdata('lolpath')) + "\config")
			id = championdata['championId']
			patch = championdata['patch']
			lane = championdata['role'].strip("DUO_").title()
			name,title = itemset.getchampname(id)
			winRate = round(championdata['winRate']*100,2)

			title = "{}-{}-{}%".format(lane,title,winRate)

			frequentitems = championdata['hashes']['finalitemshashfixed']['highestCount']['hash'].split('-')[1:]
			frequentitemswr = round(championdata['hashes']['finalitemshashfixed']['highestCount']['winrate']*100,2)
			frequentitemsgm = championdata['hashes']['finalitemshashfixed']['highestCount']['count']

			highestwritems = championdata['hashes']['finalitemshashfixed']['highestWinrate']['hash'].split('-')[1:]
			highestwritemswr = round(championdata['hashes']['finalitemshashfixed']['highestWinrate']['winrate']*100,2)
			highestwritemsgm = championdata['hashes']['finalitemshashfixed']['highestWinrate']['count']

			frequentskillorder = str(championdata['hashes']['skillorderhash']['highestCount']['hash'])[6:]
			highestwrskillorder = str(championdata['hashes']['skillorderhash']['highestWinrate']['hash'])[6:]

			frequenttrinket = championdata['hashes']['trinkethash']['highestCount']['hash']
			highestwrtrinket = championdata['hashes']['trinkethash']['highestWinrate']['hash']

			frequentfirstitems = championdata['hashes']['firstitemshash']['highestCount']['hash'].split('-')[1:]+[frequenttrinket]
			frequentfirstitemswr = round(championdata['hashes']['firstitemshash']['highestCount']['winrate']*100,2)
			frequentfirstitemsgm = championdata['hashes']['firstitemshash']['highestCount']['count']

			highestwrsfirstitems = championdata['hashes']['firstitemshash']['highestWinrate']['hash'].split('-')[1:]+[highestwrtrinket]
			highestwrsfirstitemswr = round(championdata['hashes']['firstitemshash']['highestWinrate']['winrate']*100,2)
			highestwrsfirstitemsgm = championdata['hashes']['firstitemshash']['highestWinrate']['count']

			lolitemset={
				"title": title,
				"type": "custom",
				"map": "SR",
				"mode": "any",
				"priority": False,
				"sortrank": 1,
				"champion": name,
				"blocks": [
					{
						"items": formatitems(frequentfirstitems),
						"type": "Most Frequent Start => {}% Win Rate | {} Games".format(frequentfirstitemswr,frequentfirstitemsgm)
					},
					{
						"items": formatitems(highestwrsfirstitems),
						"type": "Highest Win % Start => {}% Win Rate | {} Games".format(highestwrsfirstitemswr,highestwrsfirstitemsgm)
					},
					{
						"items": formatitems(frequentitems),
						"type": "Most Frequent Build => {}% Win Rate | {} Games".format(frequentitemswr,frequentitemsgm)
					},
					{
						"items": formatitems(highestwritems),
						"type": "Highest Win % Build => {}% Win Rate | {} Games".format(highestwritemswr,highestwritemsgm)
					},
					{
						"items": [
							{
								"count": 1,
								"id": "3340"
							},
							{
								"count": 1,
								"id": "3341"
							},
							{
								"count": 1,
								"id": "3364"
							},
							{
								"count": 1,
								"id": "3363"
							},
							{
								"count": 1,
								"id": "2055"
							},
							{
								"count": 1,
								"id": "3187"
							},
							{
								"count": 1,
								"id": "3185"
							}
						],
						"type": "Most Frequent Skill order {}".format(frequentskillorder)
					},
					{
						"items": [
							{
								"count": 1,
								"id": "2003"
							},
							{
								"count": 1,
								"id": "2031"
							},
							{
								"count": 1,
								"id": "2033"
							},
							{
								"count": 1,
								"id": "2138"
							},
							{
								"count": 1,
								"id": "2139"
							},
							{
								"count": 1,
								"id": "2140"
							},
							{
								"count": 1,
								"id": "2047"
							}
						],
						"type": "Highest Win % Skill order {}".format(highestwrskillorder)
					}
				]
			}


			#print(lolitemset)


			championdatapath = "Champions\{}\Recommended\{}-{}-{}.json".format(itemset.clear(name),name,lane,patch)

			name = itemset.clear(name)

			if not os.path.isdir('Champions'):
				os.mkdir('Champions')
			if not os.path.isdir("Champions/{}".format(name)):
				os.mkdir("Champions/{}".format(name))
			if not os.path.isdir("Champions/{}/Recommended".format(name)):
				os.mkdir("Champions/{}/Recommended".format(name))

			with open(championdatapath,'w') as f:
				#print(championdatapath)
				json.dump(lolitemset,f,indent = 2, separators = (',', ': '))

			#deleteold(name,lane)



time.sleep(1)

elos = ['BRONZE','SILVER','GOLD','PLATINUM',False]

for elo in tqdm(elos):
	builditeamset(elo)
