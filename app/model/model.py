from flask import Flask, request, jsonify
from utilities.utils import make_prediction
import pickle
import logging

# Логування
logging.basicConfig(level=logging.INFO)

# Завантаження моделі та масштабувальника
with open('./models/random_forest_model_1.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('./models/scaler1.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)


app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    logging.info("Received request: %s", request.json)
    data = request.json

    if not data or 'features' not in data or not isinstance(data['features'], list):
        return jsonify({'error': 'Invalid input data'}), 400
    
    try:
        prediction = make_prediction(model, scaler, data)
        logging.info("Prediction successful")
        return jsonify({'predictions': prediction.tolist()})
    except ValueError as e:
        logging.error("Prediction error: %s", str(e))
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logging.error("Unexpected error: %s", str(e))
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
