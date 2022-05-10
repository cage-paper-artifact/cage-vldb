import logging
import json
import pickle as pkl
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    j = req.get_json()
    #l = json.loads(j)
    data = json.loads(j)
    pddata = pd.json_normalize(data)
    logging.info('pandas dataframe shape: ' + str(pddata.shape))
    labels = pddata[pddata.columns[20]]
    y = labels.values
    pddata.drop(pddata.columns[[0,1,2,5,6,11,12,13,16,17,20]], axis=1, inplace=True)
    indices_to_keep = ~pddata.isin([np.nan, np.inf, -np.inf]).any(1)
    newx = pddata[indices_to_keep].astype(np.float64)
    newy = y[indices_to_keep].astype(np.float64)
    newy[np.where(np.isnan(newy))] = 0
    headers = {
        "Content-type": "application/json",
        "Access-Control-Allow-Origin": "*"
    }
    if newx.shape[0] == 0:
        return func.HttpResponse("no model", headers = headers)

    reg = LinearRegression().fit(newx, newy)

    #from https://stackoverflow.com/questions/48328012/python-scikit-learn-to-json
    modeldata = {}
    modeldata['init_params'] = reg.get_params()
    modeldata['model_params'] = mp = {}
    for p in ('coef_', 'intercept_'):
        mp[p] = getattr(reg, p).tolist()
    jsonstr = json.dumps(modeldata)
    

    return func.HttpResponse(jsonstr, headers = headers)

