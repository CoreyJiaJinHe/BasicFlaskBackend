#Student: Corey He
#ID: 217253527

#There are del statements throughout the code to save memory. My laptop couldn't handle it otherwise.
#Repurposed from assignment 3 for group project's wiki files and index-json file.

#Importing Python libraries
import bs4 as BeautifulSoup
import urllib.request 
import os.path
import re
import Levenshtein as lev
import json
import time

countries=[]
url=['https://en.wikipedia.org/wiki/Canada', #0
    'https://en.wikipedia.org/wiki/China', #1
        'https://en.wikipedia.org/wiki/United_States', #2
         'https://en.wikipedia.org/wiki/Korea', #3
        'https://en.wikipedia.org/wiki/United_Kingdom', #4 
        'https://en.wikipedia.org/wiki/France', #5
        'https://en.wikipedia.org/wiki/Turkey', #6
        'https://en.wikipedia.org/wiki/Italy', #7
        'https://en.wikipedia.org/wiki/Brazil', #8
        'https://en.wikipedia.org/wiki/India', #9
        'https://en.wikipedia.org/wiki/Spain', #10
        'https://en.wikipedia.org/wiki/Australia', #11
        'https://en.wikipedia.org/wiki/Chad', #12
        'https://en.wikipedia.org/wiki/Finland'] #13'''
for count in range(len(url)):
    country=url[count]
    country=country[country.rindex('/')+1:]
    countries.append(country)

filelinks=[]
#make file links
for count in range(len(countries)):
    filelinks.append((str(countries[count]))+".html")


#scrape wikipedia
def scrape_wikipedia():
    for count in range (len(url)):
        time.sleep(1)
        get_data = urllib.request.urlopen(url[count])

        html = get_data.read()
        parse_page = BeautifulSoup.BeautifulSoup(html,'html.parser')

        with open((("./data/"+str(countries[count]))+".html"), "w", encoding = 'utf-8') as file: 
            file.write(str(parse_page.prettify()))
    del html
scrape_wikipedia()



descriptioncontent=[]
#store the first description paragraphs
for count in range (len(url)):
    with open("./data/"+filelinks[count], encoding='utf8') as html:
        parse_page = BeautifulSoup.BeautifulSoup(html, 'html.parser')

    allparagraphs=parse_page.find_all('p')
    page_content=''
    thefirstparagraph=[]
    # Looping through each of the paragraphs and adding them to the variable
    for p in allparagraphs:
        if not(p.text=='' or p.text=='\n'):
            page_content += p.text
            page_content=page_content.lstrip("\n")
            x=p.text.replace("\n",'')
            x=re.sub(r'\s+',' ',x)
            x=re.sub(r'\s+\.','.',x)
            x=re.sub(r'\s+\,',',',x)
            x=x.strip()
            thefirstparagraph.append(str(x))
    if (count== 4 or count==5 or count==7 or count ==10 or count==13):
        descriptioncontent.append(str(thefirstparagraph[1]))
    else:
        descriptioncontent.append(str(thefirstparagraph[0]))
    page_content=[]
del thefirstparagraph
del allparagraphs
del parse_page
del x
del BeautifulSoup
del html

#display first paragraph descriptions
'''def print_page_descriptions():
    for count in range(len(descriptioncontent)):
        print(descriptioncontent[count])
        print("\n")
print_page_descriptions()
'''

#create inverted word index
firstline=""
wordindex=dict()
for firstpage in range(len(descriptioncontent)):
    firstline=str(descriptioncontent[firstpage])
    bracket=["(", "[","  "]
    for bracket in firstline:
        if (re.search(r'\(.*\)',firstline)):
            firstline=firstline[0:firstline.index("(")] +" "+ firstline[firstline.index(")")+1:]
        if (re.search(r'\[.*\]',firstline)):
            firstline=firstline[0:firstline.index("[")] +" "+ firstline[firstline.index("]")+1:]
        firstline=re.sub(r'\s{2}','',firstline)
    firstline=re.sub(r"'s|\.|\," ,'',firstline)
    firstline=re.sub(r"\-",' ',firstline)
    firstline=re.sub(r"\;",' ',firstline)
    firstline=firstline.lower()
    linesplit=firstline.split(" ")

    for word in range(len(linesplit)):
        if (not wordindex or not (linesplit[word] in wordindex)):
            wordindex[linesplit[word]]=[[countries[firstpage],word]]
        else:
            oldwordindex=(wordindex[linesplit[word]])
            oldwordindex.append([countries[firstpage],word])
            wordindex[linesplit[word]] = oldwordindex
del firstline
del oldwordindex
        
#clean index of small copulas
uselesswords={'is', 'its','a','in','and','are','any','an','as','at','the','to'}
for k in uselesswords:
    wordindex.pop(k,None)
del uselesswords

#make an index of occurrence frequency using the inverted index
'''
wordcount=dict()
for k in wordindex:
    wordindexvaluelist=(wordindex[k])
    wordcount[k]=len(wordindexvaluelist)
    del wordindexvaluelist
'''


with open('./index/inverted_index.json','w') as fp:
    json.dump(wordindex,fp)

#print(wordcount)
print(wordindex)
