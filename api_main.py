import pandas as pd
import pickle
from flask import Flask, request , jsonify, render_template

app = Flask(__name__)

with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('encoder.pkl', 'rb') as file:
    encoder = pickle.load(file)



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods = ['POST'])
def predict():
    data = request.get_json()
    
    required_features = ['session_time', 'pages_viewed', 'past_visits', 'traffic_source', 'user_device']
    
    if not all(feature in data for feature in required_features):
        return jsonify({'error: Missing some features! Need :' + ',' .join(required_features)}) , 400
    
    valid_sources = ['direct', 'referral', 'ads']
    valid_devices = ['Mobile', 'Desktop']
    
    if data['traffic_source'] not in valid_sources:
        return jsonify({'error': f'traffic_source must be one of : { ',' .join(valid_sources)}'}), 400
    
    if data['user_device'] not in valid_devices:
        return jsonify({'error': f"valid devices must be one of : { ','.join(valid_devices)}"}), 400


#validating the numeric features
    try:
        session_time = float(data['session_time'])
        pages_viewed = int(data['pages_viewed'])
        past_visits = int(data['past_visits'])
        if session_time < 0 or pages_viewed < 0 or past_visits < 0:
            return jsonify({'error' : 'Numeric features must be non negative numbers'}), 400
    except (ValueError, TypeError):
        return jsonify({'error':'Numeric features must be valid numbers '}), 400


# Create a DataFrame for the input data
    input_data = pd.DataFrame({
        'session_time': [session_time],
        'pages_viewed': [pages_viewed],
        'past_visits': [past_visits],
        'traffic_source': [data['traffic_source']],
        'user_device': [data['user_device']]
        
    })
    
    
    # Preprocess the input
    # Encode categorical features
    
    encoded_features = encoder.transform(input_data[['traffic_source', 'user_device']])
    encoded_columns = encoder.get_feature_names_out(['traffic_source', 'user_device'])
    encoded_data = pd.DataFrame(encoded_features , columns = encoded_columns)
    
    #combine with numeric features
    number_features = input_data[['session_time','pages_viewed','past_visits']]
    all_features = pd.concat([number_features, encoded_data], axis = 1)



    prediction = model.predict(all_features)[0]
    
    result = 'Convert' if prediction ==1 else 'Bounce'


    return jsonify ({
        'prediction' : result,
        'converted'  : int(prediction) 
    })
    


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5500)

