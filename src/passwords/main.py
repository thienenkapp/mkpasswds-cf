import functions_framework
from google.cloud import firestore
import json
import random

wordfiles=[]
wordsnoun=[]
wordsverb=[]
wordsadjective=[]
wordsnum=[0,1,2,3,4,5,6,7,8,0]
wordsseperator=['.','-','_','+','*','/','|',',',';',':']
wordsspecialchar=['!','?','$','&']
passwords_return=[]

def log(message,level):
    if level < 1:
        print(message)
    elif level < 2:
        print(message)

def ReadWordFile(sCollection, countryFilter=['en'], categoryFilter=['all']):
    # Project ID is determined by the GCLOUD_PROJECT environment variable
    db = firestore.Client()

    users_ref = db.collection(u'mkpasswd-wordlists')
    docs = users_ref.stream()

    print("Read docs:")
    for doc in docs:
        data=doc.to_dict()
        #print(data)

        if ("country" in data):
            i=1
            #print(data["country"])
        else:
            print("No Country defined - Check")
        #print(f'{doc.id} => {doc.to_dict()}')

        useData=False
        if countryFilter=='all' or data['country'] in countryFilter:
            useData=True
            #print("Country: Ok " + data['country'])
        if (useData==True) and ((categoryFilter=="all") or (data['category']in categoryFilter)):
            useData=True
            #print("Category: Ok " + data['category'])
        else:
            useData= False

        if (useData==False):
            continue
        if ("nouns" in data):
            wordsnoun.extend(data['nouns'])
            #print(wordsnoun)
        else:
            print("No NOUN defined - Check " + data['category'])

        if ("verbs" in data):
            wordsverb.extend(data['verbs'])
            #print(wordsverb)
        else:
            print("No VERB defined - Check " + data['category'])

        if ("adjectives" in data):
            wordsadjective.extend(data['adjectives'])
            #print(wordsadjective)
        else:
            print("No ADJECTIVE defined - Check " + data['category'])

def WordCorrections(aword: str):
    #Replace space trimboth and in a word
    #Replace special characters öäüß
    replacements={' ': '', 'ß':'ss',
                  'ö':'oe', 'ä':'ae', 'ü':'ue',
                  'Ö':'Oe', 'Ä':'Ae', 'Ü':'Ue'
                }
    for i, j in replacements.items():
        aword = aword.replace(i, j)
    correction=aword.strip()
    return correction

def GetRandomElement(wordsList):
    rndgen=random.SystemRandom()
    num=rndgen.randint(1,wordsList.__len__())
    return WordCorrections(wordsList[num-1])

def GeneratePassword():
    #
    # Target is to have at least three words, special characters and numbers
    # This pices must be shaked and the dictionary words slightly modified and we have something new
    # Let's start with fixed 3 words based on the word type NOUN, VERB and ADJECTIV
    # I will go with fixed order like
    #   - NOUN VERB ADJE
    #   - NOUN NOUN NOUN
    #   - NOUN VERB NOUN
    #
    rndgen=random.SystemRandom()
    pwords=[]

    seperator=GetRandomElement(wordsseperator)

    #Part1
    pwords.append(GetRandomElement(wordsnoun))
    #Part2
    if (wordsverb.__len__()>0):
        pwords.append(GetRandomElement(wordsverb))
    else:
        #num=rndgen.randint(1,wordsnoun.__len__())
        pwords.append(GetRandomElement(wordsnoun))

    #Part3
    if (wordsadjective.__len__()>0):
        #num=rndgen.randint(1,wordsadjective.__len__())
        #genPW=genPW+seperator+wordsadjective[num-1]
        pwords.append(GetRandomElement(wordsadjective))
    else:
        #num=rndgen.randint(1,wordsnoun.__len__())
        #genPW=genPW+seperator+wordsnoun[num-1]
        pwords.append(GetRandomElement(wordsnoun))

    num=rndgen.randint(1,999)

    genPW=""
    for pword in pwords:
        genPW=genPW+pword+seperator

    genPW=genPW+str(num)+GetRandomElement(wordsspecialchar)

    #print (genPW)
    return genPW

def clean_lists():
    wordsnoun.clear()
    wordsverb.clear()
    wordsadjective.clear()
    passwords_return.clear()

def main_get_passwords(request):
    countries=[]
    categories=[]

    country = request.args.get('country', default = 'de', type = str)
    category = request.args.get('category', default = 'computer', type = str)
    number_of_password = request.args.get('number', default = 5, type = int)

    if number_of_password < 0 or number_of_password > 50:
        print("number parameter is not ok. Set default")
        number_of_password=5

    countries.append(country)
    categories.append(category)
    # ReadWordFile('mkpasswd-wordlists',['de','fr'],['ku\u0308che','funny','computer'])
    clean_lists

    ReadWordFile('mkpasswd-wordlists',countries,categories)
    if (wordsnoun.__len__()==0):
        print("No noun words found. Expect that every list has nouns")
        return 1

    for i in range (number_of_password-1):
        pwd=GeneratePassword()
        if (pwd != ""):
            passwords_return.append(dict(password = pwd))

    jsonString = json.dumps(passwords_return) #, indent=4)
    print(jsonString)
    return jsonString

@functions_framework.http
def main(request):
    # For more information about CORS and CORS preflight requests, see:
    # https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request

    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    return (main_get_passwords(request), 200, headers)
