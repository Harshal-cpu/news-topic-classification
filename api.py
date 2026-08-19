"""
Flask REST API for News Topic Classification
Provides endpoint for real-time predictions
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from utils import TextPreprocessor

app = Flask(__name__)
CORS(app)

# Global variables for model and vectorizer
model = None
vectorizer = None
category_names = None
preprocessor = None


def train_and_save_model():
    """Train model and save for API use"""
    print("Training model for API...")
    
    # Load data
    train_data = fetch_20newsgroups(
        subset='train',
        shuffle=True,
        random_state=42,
        remove=('headers', 'footers', 'quotes')
    )
    
    # Preprocess
    global preprocessor, category_names
    preprocessor = TextPreprocessor(use_lemmatization=True)
    X_train_clean = [preprocessor.preprocess(text) for text in train_data.data]
    category_names = train_data.target_names
    
    # Vectorize
    global vectorizer
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2), min_df=2)
    X_train_vec = vectorizer.fit_transform(X_train_clean)
    
    # Train
    global model
    model = LinearSVC(random_state=42, C=1.0, max_iter=2000)
    model.fit(X_train_vec, train_data.target)
    
    # Save model
    os.makedirs('models', exist_ok=True)
    with open('models/model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('models/vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    with open('models/categories.pkl', 'wb') as f:
        pickle.dump(category_names, f)
    
    print("[OK] Model trained and saved!")


def load_model():
    """Load trained model"""
    global model, vectorizer, category_names, preprocessor

    model_paths = [
        ('models/news_classifier_model.pkl', 'models/news_classifier_vectorizer.pkl', 'models/news_classifier_categories.pkl'),
        ('models/model.pkl', 'models/vectorizer.pkl', 'models/categories.pkl'),
    ]

    loaded = False
    for m_path, v_path, c_path in model_paths:
        if os.path.exists(m_path) and os.path.exists(v_path) and os.path.exists(c_path):
            with open(m_path, 'rb') as f:
                model = pickle.load(f)
            with open(v_path, 'rb') as f:
                vectorizer = pickle.load(f)
            with open(c_path, 'rb') as f:
                category_names = pickle.load(f)
            loaded = True
            break

    if not loaded:
        train_and_save_model()

    preprocessor = TextPreprocessor(use_lemmatization=True)
    print("[OK] Model loaded successfully!")


@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'News Topic Classification API',
        'version': '1.0',
        'endpoints': {
            '/predict': 'POST - Predict news category',
            '/categories': 'GET - List all categories',
            '/health': 'GET - Health check'
        }
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})


@app.route('/categories')
def categories():
    """Get all categories"""
    return jsonify({'categories': list(category_names)})


@app.route('/predict', methods=['POST'])
def predict():
    """Predict news category"""
    try:
        # Get text from request
        data = request.get_json()
        
        if 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        
        if not text or len(text.strip()) == 0:
            return jsonify({'error': 'Empty text provided'}), 400
        
        # Preprocess
        cleaned_text = preprocessor.preprocess(text)
        
        # Vectorize
        text_vec = vectorizer.transform([cleaned_text])
        
        # Predict
        prediction = model.predict(text_vec)[0]
        predicted_category = category_names[prediction]
        
        # Get decision scores (confidence)
        decision_scores = model.decision_function(text_vec)[0]
        top_3_idx = decision_scores.argsort()[-3:][::-1]
        
        top_predictions = [
            {
                'category': category_names[idx],
                'confidence': float(decision_scores[idx])
            }
            for idx in top_3_idx
        ]
        
        return jsonify({
            'text': text[:200] + '...' if len(text) > 200 else text,
            'predicted_category': predicted_category,
            'top_predictions': top_predictions
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Load model at startup (runs when gunicorn imports the module too)
load_model()

if __name__ == '__main__':
    print("="*70)
    print("NEWS CLASSIFICATION API")
    print("="*70)
    
    print("\nStarting Flask server...")
    print("API available at: http://localhost:5000")
    print("\nExample usage:")
    print('   curl -X POST http://localhost:5000/predict \\')
    print('        -H "Content-Type: application/json" \\')
    print('        -d "{\\"text\\":\\"NASA launched a new satellite\\"}"')
    print("\n" + "="*70)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
