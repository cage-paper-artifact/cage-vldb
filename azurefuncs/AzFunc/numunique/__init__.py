import logging
import json
import pickle as pkl
import numpy as np

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    j = req.get_json()
    #l = json.loads(j)
    data = np.array(j)
    logging.info('data shape: ' + str(data.shape))
    res = np.sum(np.unique(data))
    
    headers = {
        "Content-type": "application/json",
        "Access-Control-Allow-Origin": "*"
    }

    return func.HttpResponse(str(res), headers = headers)

