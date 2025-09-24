from flask import Flask, render_template, jsonify, request, url_for

app = Flask(__name__)

# Mock data for each model's evaluation metrics and confusion matrix image path
# In a real-world application, this data would be loaded from a file or database.
model_data = {
    'extratrees': {
        'accuracy': '0.997',
        'precision': '0.731',
        'recall': '0.95',
        'f1_score': '0.826',
        'confusion_matrix_path': 'images/extratrees_cm.png'
    },
    'randomforest': {
        'accuracy': '0.997',
        'precision': '0.704',
        'recall': '0.95',
        'f1_score': '0.809',
        'confusion_matrix_path': 'images/randomforest_cm.png'
    },
    'xgboost': {
        'accuracy': '0.996',
        'precision': '0.613',
        'recall': '0.95',
        'f1_score': '0.745',
        'confusion_matrix_path': 'images/xgboost_cm.png'
    }
}

@app.route('/')
def home():
    """Renders the main landing page."""
    return render_template('index.html')

@app.route('/metrics')
def metrics_page():
    """Renders the metrics evaluation page."""
    return render_template('metrics.html')

@app.route('/get_results', methods=['POST'])
def get_results():
    """
    Handles the POST request from the frontend to retrieve model evaluation results.
    Returns the metrics and image path for the selected model as a JSON object.
    """
    data = request.get_json()
    model_name = data.get('model').lower()
    
    if model_name in model_data:
        # Get the data for the selected model
        model = model_data[model_name]
        
        # Use url_for to generate the correct URL for the static image
        image_url = url_for('static', filename=model['confusion_matrix_path'])
        
        # Create a new dictionary with the generated URL and return it
        response_data = {
            'accuracy': model['accuracy'],
            'precision': model['precision'],
            'recall': model['recall'],
            'f1_score': model['f1_score'],
            'confusion_matrix': image_url
        }
        return jsonify(response_data)
    else:
        # Return a 404 error if the model is not found
        return jsonify({'error': 'Model not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
