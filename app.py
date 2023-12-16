from flask import Flask, make_response, render_template, request
from markupsafe import escape
import json
import Levenshtein as lev

DEBUG=False
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def not_found(e):
    return render_template ("404.html", index='index.html')

# the function for load the inverted indexes
def get_inverted_index():
    with open("./index/inverted_index.json") as g:
        inverted_index = json.load(g)
    return inverted_index


@app.route('/search/<keyword>')
def search_page(keyword):
    pages = []
    pages=directsearch(keyword)        
    return render_template('results.html', name=keyword, countries=pages)

#The Better Search that has fuzzy and history
@app.route('/bsearch/', methods=['GET','POST'])
def bsearch():
    if (request.method =="GET"):
        return render_template('search.html')
    elif (request.method=="POST"):

        keyword = format(request.form.get('searchtext'))
        if (keyword=="history"):
            cookie = request.cookies.get("history")
            result=[]
            if not cookie:
                result.append({"Search":"There is no history."})
                
            else:
                cookiedata=cookie
                cookiedata=cookiedata.split(',')
                for searches in cookiedata:
                    result.append({"Search":searches})
            return render_template('recentsearches.html', searches=result)
        
        pages=[]
        pages=directsearch(keyword)
        res=''
        if not pages:
            closestwords=findclosest(keyword)
            pages=fuzzysearch(closestwords)
            words=[]
            for count in range(len(closestwords)):
                words.append(closestwords[count][0])
            words=', '.join(words)
            res=make_response(render_template('closestsearch.html',name=keyword,closestwords=words,countries=pages))
        else:            
            res = make_response (render_template('search.html',name=keyword, countries=pages))
        if not request.cookies.get('history'):
                res.set_cookie('history',keyword, max_age=60*60*24*365*2)
        else:
                newhistory=format(request.cookies.get('history'))+"," + keyword
                res.set_cookie('history',newhistory, max_age=60*60*24*365*2)
 
        return res
#        return render_template('search.html',name=keyword, countries=pages)

def directsearch(keyword):
    inverted_index = get_inverted_index() # get the inverted indexes
    pages=[]
    if keyword in inverted_index:
            for country in inverted_index[keyword]:
                if len(pages):
                    checkcounter=0
                    for checklist in pages:
                        if (checklist['Country']==country[0]):
                            checkcounter=1
                            break
                        else:
                            checkcounter=0
                    if (checkcounter==0):
                        pages.append({"Country":country[0],"Link":"https//en.wikipedia.org/wiki/"+str(country[0])})
                else:
                    pages.append({"Country":country[0],"Link":"https//en.wikipedia.org/wiki/"+str(country[0])})
    return pages

def fuzzysearch(similarwords):
    inverted_index=get_inverted_index()
    pages=[]
    #turns the list of closest words to actual page results
    for count in range(len(similarwords)):
        theword=similarwords[count]
        if (theword[1]<3):
            for country in inverted_index[theword[0]]:
                checkcounter=0
                if len(pages):
                    for checklist in pages:
                        if (checklist['Country']==country[0]):
                            checkcounter=1
                            break
                        else:
                            checkcounter=0
                                        
                    if (checkcounter==0):
                        pages.append({"Country":country[0],"Link":"https//en.wikipedia.org/wiki/"+str(country[0])})
                        
                else:
                    pages.append({"Country":country[0],"Link":"https//en.wikipedia.org/wiki/"+str(country[0])})
    return pages

def findclosest(keyword):
    #fuzzy search if no direct search
    listofkeys=list(inverted_index.keys())
    pairedword=[]
    for word in listofkeys:
        distance=lev.distance(keyword,word)
        if (len(pairedword)<5):
            appendstuff=[word,distance]
            pairedword.append(appendstuff)
        else:
            for count in range(len(pairedword)):
                comparedistance=list(pairedword[count])
                if (comparedistance[1]>distance):
                    pairedword[count]=[word,distance]
                    break
    return pairedword




#testing code
inverted_index=get_inverted_index()
pages = []
test=1
keyword='test'
if keyword in inverted_index:
    for country in inverted_index[keyword]:
        if len(pages):
            checkcounter=0
            for checklist in pages:
                if (checklist['Country']==country[0]):
                    checkcounter=1
                    break
                else:
                    checkcounter=0
            if (checkcounter==0):
                pages.append({"Country":country[0],"Link":"https//en.wikipedia.org/wiki/"+str(country[0])})
        else:
            pages.append({"Country":country[0],"Link":"https//en.wikipedia.org/wiki/"+str(country[0])})
else:
    listofkeys=list(inverted_index.keys())
    pairedword=[]
    for word in listofkeys:
        distance=lev.distance(keyword,word)
        if (len(pairedword)<5):
            appendstuff=[word,distance]
            pairedword.append(appendstuff)
        else:
            for count in range(len(pairedword)):
                comparedistance=list(pairedword[count])
                if (comparedistance[1]>distance):
                    pairedword[count]=[word,distance]
                    break
    for count in range(len(pairedword)):
        theword=pairedword[count]
        if (theword[1]<3):
            for country in inverted_index[theword[0]]:
                checkcounter=0
                if len(pages):
                    
                    for checklist in pages:
                        if (checklist['Country']==country[0]):
                            checkcounter=1
                            #print (checklist['Country']+"   the other:"+country[0])
                            break
                        else:
                            checkcounter=0
                            #print (checklist['Country']+"   the current country:"+country[0])                
                    if (checkcounter==0):
                        pages.append({"Country":country[0],"Link":"https//en.wikipedia.org/wiki/"+str(country[0])})
                        
                else:
                    pages.append({"Country":country[0],"Link":"https//en.wikipedia.org/wiki/"+str(country[0])})

print (pages)
