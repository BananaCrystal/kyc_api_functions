import boto3
from fuzzysearch import find_near_matches
import os
import json

sdn_lines = ''
nonsdn_lines = ''

def read_s3_file(fname):
    # get a handle on s3

    s3 = boto3.resource('s3')

    obj = s3.Object(
        bucket_name=os.getenv('BUCKET'),
        key=fname
    )
    # get the object
    try:
        response = obj.get()
        print("reading the contents of " + fname + "...")
        lines = response['Body'].read()
        print("finished reading..")
        return lines.decode().lower()
    except BaseException as e:
        print(str(e))
        return "Error: " + str(e)

def amlcheck(event, context):
    global sdn_lines
    global nonsdn_lines

    name = event['queryStringParameters'].get('name', "None")
    idno = event['queryStringParameters'].get('idno', "None")
    email = event['queryStringParameters'].get('email', "None")
    reread = event['queryStringParameters'].get('reread', "None")

    print("Name = ", name, "ID No = ", idno, "Email = ", email, "Re-read = ", reread)

    hits = 0

    responseObject = {}
    responseObject['headers'] = {}
    responseObject['headers']['Access-Control-Allow-Origin']= '*'
    responseObject['headers']['Content-type'] = 'application/json'
    transactionResponse = {}
 
    if sdn_lines == '' or reread == 'true':
        has_error = False
        nonsdn_lines = read_s3_file('cons_prim.csv')
        if nonsdn_lines.startswith("Error: "):
            transactionResponse['message'] = 'Internal Server Error. ' + nonsdn_lines
            has_error = True
        else:
            sdn_lines = read_s3_file('sdnlist.txt')
            if sdn_lines.startswith("Error: "):
                transactionResponse['message'] = 'Internal Server Error. ' + sdn_lines
                has_error = True
        if has_error:
            responseObject['statusCode'] = 500
            responseObject['body'] = json.dumps(transactionResponse)
            return responseObject
    # max_l_dist of 3 results in gateway timeout (limit is 30 seconds)
    if name != "None": 
        match_sdn = find_near_matches(name.lower(),sdn_lines, max_l_dist=2)
        match_nonsdn = find_near_matches(name.lower(),nonsdn_lines, max_l_dist=2)
        hit = len(match_sdn) + len(match_nonsdn)
        print("Name Check Hits = ", hit)
        hits += hit

    if idno != "None":
        match_sdn = find_near_matches(idno.lower(),sdn_lines, max_l_dist=0)
        match_nonsdn = find_near_matches(idno.lower(),nonsdn_lines, max_l_dist=0)
        hit = len(match_sdn) + len(match_nonsdn)
        print("ID Check Hits = ", hit)
        hits += hit

    if email != "None":
        match_sdn = find_near_matches(email.lower(),sdn_lines, max_l_dist=0)
        match_nonsdn = find_near_matches(email.lower(),nonsdn_lines, max_l_dist=0)
        hit = len(match_sdn) + len(match_nonsdn)
        print("Email Check Hits = ", hit)
        hits += hit

    transactionResponse['hits'] = str(hits)

    responseObject['statusCode'] = 200
    responseObject['body'] = json.dumps(transactionResponse)

    return responseObject
    

