import requests
import json



def getInput(title):
    url='https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exsentences=3&titles=%s&exsectionformat=plain&formatversion=2' % title
    response = requests.get(url)
    data=json.loads(response.content)
    extract=data['query']['pages'][0]['extract']
    print("hello")
    if str(extract).find('refer') != -1:
        return parseExtract2(extract)
    else:
        return None
    



def parseExtract2(extract):
    extract=str(extract)
    
    j=extract.find('<')

    while j!=-1:
        endOne=extract.find('>')
        extract=extract[:j]+extract[endOne+1:]
        
        j=extract.find('<')
    return extract

