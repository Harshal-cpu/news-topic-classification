"""
Utility functions for News Topic Classification
Contains text preprocessing and helper functions
"""

import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download required NLTK data
NLTK_RESOURCES = {
    'corpora/stopwords': 'stopwords',
    'tokenizers/punkt': 'punkt',
    'tokenizers/punkt_tab': 'punkt_tab',
    'corpora/wordnet': 'wordnet',
}

for resource_path, resource_name in NLTK_RESOURCES.items():
    try:
        nltk.data.find(resource_path)
    except LookupError:
        nltk.download(resource_name, quiet=True)


class TextPreprocessor:
    """Text preprocessing pipeline for news classification"""
    
    def __init__(self, use_lemmatization=True):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer() if use_lemmatization else None
    
    def clean_text(self, text):
        """Clean and preprocess text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Remove numbers
        text = re.sub(r'\d+', '', text)
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def tokenize_and_filter(self, text):
        """Tokenize and remove stopwords"""
        tokens = word_tokenize(text)
        tokens = [word for word in tokens if word not in self.stop_words and len(word) > 2]
        
        if self.lemmatizer:
            tokens = [self.lemmatizer.lemmatize(word) for word in tokens]
        
        return ' '.join(tokens)
    
    def preprocess(self, text):
        """Complete preprocessing pipeline"""
        text = self.clean_text(text)
        text = self.tokenize_and_filter(text)
        return text


def get_top_features(vectorizer, classifier, category_names, n=10):
    """
    Extract top N features (words) for each category
    
    Args:
        vectorizer: Fitted vectorizer (CountVectorizer or TfidfVectorizer)
        classifier: Trained classifier
        category_names: List of category names
        n: Number of top features to extract
    
    Returns:
        Dictionary mapping category to top features
    """
    feature_names = vectorizer.get_feature_names_out()
    top_features = {}
    
    if hasattr(classifier, 'coef_'):
        # For linear models (Logistic Regression, SVM)
        for i, category in enumerate(category_names):
            top_indices = classifier.coef_[i].argsort()[-n:][::-1]
            top_features[category] = [feature_names[idx] for idx in top_indices]
    elif hasattr(classifier, 'feature_log_prob_'):
        # For Naive Bayes
        for i, category in enumerate(category_names):
            top_indices = classifier.feature_log_prob_[i].argsort()[-n:][::-1]
            top_features[category] = [feature_names[idx] for idx in top_indices]
    
    return top_features


def print_top_features(top_features, n_categories=5):
    """Print top features for selected categories"""
    print("\n" + "="*70)
    print("TOP FEATURES (WORDS) PER CATEGORY")
    print("="*70)
    
    for i, (category, features) in enumerate(list(top_features.items())[:n_categories]):
        print(f"\n📌 {category}:")
        print(f"   {', '.join(features)}")


def format_category_name(category):
    """Format category name for better readability"""
    return category.replace('.', ' > ').title()
