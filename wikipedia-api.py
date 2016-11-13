import requests
import json


def main():
    #print("Which article do you want to try")
    #title=raw_input()
    #url='https://en.wikipedia.org/w/api.php?action=query&format=json&prop=short-summary&list=&meta=&titles=%s' % title
    title=getInput()
    url='https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exsentences=3&titles=%s&exsectionformat=plain&formatversion=2' % title
    response = requests.get(url)
    #data = response.json()
    data=json.loads(response.content)
        extract=data['query']['pages'][0]['extract']

        summary=parseExtract2(extract)
    #with open ('data3.json','w') as outfile:
     #   json.dump(data,outfile)
    #print(data)

def getInput():
    j=-1
    while j==-1:
        title=raw_input()
        

def parseExtract2(extract):
    extract=str(extract)
    
    j=extract.find('<')
    print(extract,j)

    while j!=-1:
        endOne=extract.find('>')
        extract=extract[:j]+extract[endOne+1:]
        
        j=extract.find('<')
    return extract


if __name__ == '__main__':
  main()