import logging

import azure.functions as func

import pronouncing
import json



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    MAPPING = {
        'AA0':'aa',
        'AA1':'aa',
        'AA2':'aa',
        'AE0':'a',
        'AE1':'a',
        'AE2':'a',
        'AH0':'ah',
        'AH1':'ah',
        'AH2':'ah',
        'AO0':'ao',
        'AO1':'ao',
        'AO2':'ao',
        'AW0':'aw',
        'AW1':'aw',
        'AW2':'aw',
        'AY0':'ay',
        'AY1':'ay',
        'AY2':'ay',
        'EH0':'eh',
        'EH1':'eh',
        'EH2':'eh',
        'ER0':'er',
        'ER1':'er',
        'ER2':'er',
        'EY0':'ey',
        'EY1':'ey',
        'EY2':'ey',
        'IH0':'ih',
        'IH1':'ih',
        'IH2':'ih',
        'IY0':'iy',
        'IY1':'iy',
        'IY2':'iy',
        'OW0':'ow',
        'OW1':'ow',
        'OW2':'ow',
        'OY0':'oy',
        'OY1':'oy',
        'OY2':'oy',
        'UH0':'uh',
        'UH1':'uh',
        'UH2':'uh',
        'UW0':'uw',
        'UW1':'uw',
        'UW2':'uw'
    }

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
            pronunciation_characters = []
            phonetics = pronouncing.phones_for_word(name)
            logging.info("Phonetic Spelling: %s" % phonetics)
        
            for phonetic in phonetics:
                phonetic_characters = phonetic.split()
                for character in phonetic_characters:
                    if character in MAPPING:
                        pronunciation_characters.append(MAPPING[character])
                    else:
                        pronunciation_characters.append(character)

                break
            
            delimiter = '-'
            pronunciation = delimiter.join(pronunciation_characters)
            pronunciation.lower()
        except ValueError:
            func.HttpResponse(status_code=500)

        return func.HttpResponse(json.dumps(pronunciation),status_code=200)
    else:
        return func.HttpResponse(status_code=400)
