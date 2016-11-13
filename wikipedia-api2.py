import requests
import json

title='Journey'
#url='https://en.wikipedia.org/w/api.php?action=query&format=json&prop=short-summary&list=&meta=&titles=%s' % title
url='https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exsentences=3&titles=%s&exsectionformat=plain&formatversion=2' % title
response = requests.get(url)
#data = response.json()
data=json.loads(response.content)
print(data)