import boto3
from fuzzysearch import find_near_matches
import os
import json

sdn_lines = ''
nonsdn_lines = ''

def read_s3_file(fname):
    # get a handle on s3
    session = boto3.Session(
                    aws_access_key_id=os.environ['ACCESS_KEY'],
                    aws_secret_access_key=os.environ['SECRET_KEY'],
                    region_name=os.environ['REGION_NAME'])
                    
    s3 = session.resource('s3')

    # get a handle on the bucket that holds your file
    bucket = s3.Bucket('opendax-aml-bucket') 

    # get a handle on the object you want (i.e. your file)
    obj = bucket.Object(key=fname) 

    # get the object
    response = obj.get()
    print("reading the contents of " + fname + "...")
    lines = response['Body'].read()
    print("finished reading..")
    return lines.decode().lower()

def amlcheck(event, context):
    global sdn_lines
    global nonsdn_lines

    name = event['queryStringParameters'].get('name', "None")
    idno = event['queryStringParameters'].get('idno', "None")
    email = event['queryStringParameters'].get('email', "None")
    reread = event['queryStringParameters'].get('reread', "None")

    print("Name = ", name)
    print("ID No = ", idno)
    print("Email = ", email)
    print("Re-read = ", reread)

    hits = 0

    if sdn_lines == '' or reread == 'true':
        nonsdn_lines = read_s3_file('cons_prim.csv')
        sdn_lines = read_s3_file('sdnlist.txt')

    if name != "None": 
        match_sdn = find_near_matches(name.lower(),sdn_lines, max_l_dist=3)
        match_nonsdn = find_near_matches(name.lower(),nonsdn_lines, max_l_dist=3)
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

    transactionResponse = {}
    transactionResponse['hits'] = str(hits)

    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-type'] = 'application/json'
    responseObject['body'] = json.dumps(transactionResponse)

    return responseObject
    

