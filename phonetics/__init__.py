import azure.functions as func

import logging
import json
import requests
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Retrieve the name from the GET parameter
    name = req.params.get('name')
    logging.info("Name: %s" % name)

    # Define a list of our API tokens using settings variables
    nameshout_api_tokens = [
        os.environ.get('NAMESHOUT_API_TOKEN_MM'),
        os.environ.get('NAMESHOUT_API_TOKEN_MMNHS'),
        os.environ.get('NAMESHOUT_API_TOKEN_A'),
        os.environ.get('NAMESHOUT_API_TOKEN_AE'),
        os.environ.get('NAMESHOUT_API_TOKEN_NP'),
        os.environ.get('NAMESHOUT_API_TOKEN_DG'),
        os.environ.get('NAMESHOUT_API_TOKEN_SIdB')
    ]

    # If no name was detected check the request body
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    # If the name has now been found
    if name:
        # Check if a string
        if not isinstance(name,str):
            return func.HttpResponse(status_code=400)
        # Check if it's a reasonable length
        if not 0 < len(name) <= 255:
            return func.HttpResponse(status_code=400)

        # Attempt to create a phonetical translation
        try:
            # Set base string which shall be returned if translation does not work
            pronunciation = ""
            nameshout_success = False

            # Cycle through each of the nameshout api tokens - some may have no more free executions
            for bearer_token in nameshout_api_tokens:

                # Create the HTTP request
                url = "https://api.nameshouts.com/api/v2.0/name/%s/english" % name
                headers = {
                    'Authorization': "Bearer %s" % bearer_token,
                    'Content-Type': "application/x-www-form-urlencoded"
                }

                nameshout_response = requests.get(url, headers=headers)
                
                # Determine response
                if nameshout_response.status_code == 200:
                    json_response = nameshout_response.json()

                    # Check if request limit has been reached
                    if 'search_limit_reached' in json_response:
                        if json_response['search_limit_reached'] is True:
                            logging.info('Bearer token capacity reached')

                    else:
                        logging.info('Bearer token has capacity')
                        # If not reached limit, then retrieve name then break for loop so that current phonetical spelling is returned
                        name_res = json_response['name_res']
        
                        if len(name_res) > 0:
                            pronunciation = name_res[0]['name_phonetic']

                        nameshout_success = True

                        break

            if nameshout_success is False:
                logging.info("Nameshout has no capacity")

        except ValueError:
            func.HttpResponse(status_code=500)

        logging.info("Returned Name: %s" % pronunciation)
        return func.HttpResponse(json.dumps(pronunciation),status_code=200)
    else:
        return func.HttpResponse(status_code=400)
