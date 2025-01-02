import numpy as np

def data_preprocess(scaler, data):
    features = data.get('features', [])
    if not features or len(features[0]) < 1:
        raise ValueError("Input data is missing or incomplete")
    
    raw_features = features[0]
    type_of_work = raw_features[-1]
    data_to_scale = raw_features[:-1]
    scaled_data = scaler.transform([data_to_scale])
    processed_data = np.append(scaled_data, type_of_work)
    return processed_data

def make_prediction(model, scaler, data):
    processed_data = data_preprocess(scaler, data)
    prediction = model.predict([processed_data])
    return prediction
