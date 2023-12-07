import azure.functions as func

import logging
import json
import requests
import os

NAMESHOUT_API_TOKEN = os.environ.get('NAMESHOUT_API_TOKEN')

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    logging.info("Name: %s" % name)

    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:

        if not isinstance(name,str):
            return func.HttpResponse(status_code=400)
        
        if not 0 < len(name) <= 255:
            return func.HttpResponse(status_code=400)

        try:
            pronunciation = ""
            bearer_token = NAMESHOUT_API_TOKEN
            url = "https://api.nameshouts.com/api/v2.0/name/%s/english" % name
            headers = {
                'Authorization': "Bearer %s" % bearer_token,
                'Content-Type': "application/x-www-form-urlencoded"
            }

            nameshout_response = requests.get(url, headers=headers)

            if nameshout_response.status_code == 200:

                json_response = nameshout_response.json()
                name_res = json_response['name_res']
   
                if len(name_res) > 0:
                    pronunciation = name_res[0]['name_phonetic']

        except ValueError:
            func.HttpResponse(status_code=500)

        return func.HttpResponse(json.dumps(pronunciation),status_code=200)
    else:
        return func.HttpResponse(status_code=400)
