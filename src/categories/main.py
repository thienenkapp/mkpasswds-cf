#!/usr/bin/python3
import functions_framework
from google.cloud import firestore
import json

categories_a=[]
categories_r=[]

def ReadCategories(sCollection):
    # Project ID is determined by the GCLOUD_PROJECT environment variable
    db = firestore.Client()

    users_ref = db.collection(u'mkpasswd-wordlists')
    docs = users_ref.stream()

    #print("Read docs:")
    for doc in docs:
        data=doc.to_dict()
        #print(data)

        if ("category" in data):
            if (data["category"] not in categories_a):
                categories_a.append(data["category"])
                categories_r.append(dict(name = data["category"]))
                #print(data["category"])
                #print(categories)


def main_get_categories(request):
    ReadCategories('mkpasswd-wordlists')
    jsonString = json.dumps(categories_r) #, indent=4)
    print(jsonString)
    return jsonString
#
# CORS was needed because local Swagger development was able to connect
# It could be solved in LoadBalancer, in Backend (StackDriver) or NEG.
# It must be done in the function itself
# https://cloud.google.com/functions/docs/samples/functions-http-cors
#

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


    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    if request.args and 'message' in request.args:
        return (request.args.get('message'), 200, headers)
    elif request_json and 'message' in request_json:
        return (request_json['message'], 200, headers)
    else:
        return (main_get_categories(request), 200, headers)
