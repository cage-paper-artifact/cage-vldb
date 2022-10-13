"""
The simpliest UDF ever
Args:
    model: A SKL or pytorch model
    data: a numpy array

Returns:
    A numpy array of the predictions from the model
"""
def run(model, data):
    import pickle as pkl

    loaded_model = pkl.load(open(model, 'rb'))
    return loaded_model.predict(data)

