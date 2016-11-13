import requests
import json

# New York,Skyscraper,Hoodie Allen,Laptop,
def main():
    extract=getInput()
    summary=parseExtract2(extract)
    print(summary)

def getInput():
    j=-1
    print("What article would you like to read?")
    while j==-1:       
        title=raw_input()
        url='https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exsentences=3&titles=%s&exsectionformat=plain&formatversion=2' % title
        response = requests.get(url)
        data=json.loads(response.content)
        extract=data['query']['pages'][0]['extract']
        if str(extract).find('refer') == -1:
            print(" did not find refer")
            j=0
        print("Sorry, but the article you requested does not exist. Please suggest an alternate title.")

    return extract



def parseExtract2(extract):
    extract=str(extract)
    
    j=extract.find('<')

    while j!=-1:
        endOne=extract.find('>')
        extract=extract[:j]+extract[endOne+1:]
        
        j=extract.find('<')
    return extract


if __name__ == '__main__':
  main()