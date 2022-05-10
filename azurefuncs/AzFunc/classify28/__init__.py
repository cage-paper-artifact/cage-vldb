import logging
import json
import pickle as pkl
import numpy as np

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    model = pkl.load(open('/home/site/wwwroot/models/skl/rf10.skl','rb'))
    j = req.get_json()
    #l = json.loads(j)
    data = np.array(j)
    logging.info('np shape: ' + str(data.shape))
    preds = model.predict(data).tolist()
    
    headers = {
        "Content-type": "application/json",
        "Access-Control-Allow-Origin": "*"
    }

    return func.HttpResponse(json.dumps(preds), headers = headers)

