import requests
import json


def main():
    #print("Which article do you want to try")
    #title=raw_input()
    title='Gold'
    #url='https://en.wikipedia.org/w/api.php?action=query&format=json&prop=short-summary&list=&meta=&titles=%s' % title
    url='https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exsentences=3&titles=%s&exsectionformat=plain&formatversion=2' % title
    response = requests.get(url)
    #data = response.json()
    data=json.loads(response.content)
    extract=data['query']['pages'][0]['extract']
    summary=parseExtract(extract)

    #with open ('data3.json','w') as outfile:
     #   json.dump(data,outfile)
    #print(data)

def parseExtract(extract):
    extract=str(extract)
    index=extract.find('<p><b>')
    i=index+6
    extract=extract[i:]
    print(type(extract))
    j=extract.find('</b>')
    print(extract,j)
    while j != -1:
        extract=extract[:j]+extract[j+3:]
        j=extract.find('<b>')
        print(j)
    print(extract)

if __name__ == '__main__':
  main()