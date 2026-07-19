"""
Test script to verify installation and setup
Run this before the main project to ensure everything works
"""

import sys

def test_imports():
    """Test if all required libraries are installed"""
    print("="*70)
    print("TESTING LIBRARY IMPORTS")
    print("="*70)
    
    libraries = [
        ('numpy', 'np'),
        ('pandas', 'pd'),
        ('matplotlib.pyplot', 'plt'),
        ('seaborn', 'sns'),
        ('sklearn', None),
        ('nltk', None),
        ('flask', None)
    ]
    
    failed = []
    
    for lib, alias in libraries:
        try:
            if alias:
                exec(f"import {lib} as {alias}")
            else:
                exec(f"import {lib}")
            print(f"[OK] {lib:30s} - OK")
        except ImportError as e:
            print(f"[FAIL] {lib:30s} - FAILED")
            failed.append(lib)
    
    if failed:
        print(f"\n[X] Failed to import: {', '.join(failed)}")
        print("\nInstall missing libraries:")
        print("pip install -r requirements.txt")
        return False
    else:
        print("\n[SUCCESS] All libraries imported successfully!")
        return True


def test_nltk_data():
    """Test if NLTK data is downloaded"""
    print("\n" + "="*70)
    print("TESTING NLTK DATA")
    print("="*70)
    
    import nltk
    
    datasets = ['stopwords', 'punkt', 'wordnet', 'omw-1.4']
    failed = []
    
    for dataset in datasets:
        try:
            if dataset == 'stopwords':
                nltk.data.find('corpora/stopwords')
            elif dataset == 'punkt':
                nltk.data.find('tokenizers/punkt')
            elif dataset == 'wordnet':
                nltk.data.find('corpora/wordnet')
            elif dataset == 'omw-1.4':
                nltk.data.find('corpora/omw-1.4')
            print(f"[OK] {dataset:30s} - OK")
        except LookupError:
            print(f"[FAIL] {dataset:30s} - NOT FOUND")
            failed.append(dataset)
    
    if failed:
        print(f"\n[X] Missing NLTK data: {', '.join(failed)}")
        print("\nDownload missing data:")
        print("python -c \"import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')\"")
        return False
    else:
        print("\n[SUCCESS] All NLTK data available!")
        return True


def test_sklearn_dataset():
    """Test if sklearn can fetch dataset"""
    print("\n" + "="*70)
    print("TESTING DATASET ACCESS")
    print("="*70)
    
    try:
        from sklearn.datasets import fetch_20newsgroups
        
        print("Fetching sample data (this may take a moment)...")
        data = fetch_20newsgroups(
            subset='train',
            categories=['comp.graphics', 'sci.space'],
            shuffle=True,
            random_state=42,
            remove=('headers', 'footers', 'quotes')
        )
        
        print(f"[OK] Dataset fetched successfully")
        print(f"  - Samples: {len(data.data)}")
        print(f"  - Categories: {len(data.target_names)}")
        print(f"  - Category names: {data.target_names}")
        print("\n[SUCCESS] Dataset access working!")
        return True
    except Exception as e:
        print(f"[FAIL] Failed to fetch dataset: {e}")
        print("\n[X] Dataset access failed!")
        return False


def test_preprocessing():
    """Test text preprocessing"""
    print("\n" + "="*70)
    print("TESTING TEXT PREPROCESSING")
    print("="*70)
    
    try:
        from utils import TextPreprocessor
        
        preprocessor = TextPreprocessor(use_lemmatization=True)
        
        test_text = "Hello World! This is a TEST of the preprocessing system. Email: test@example.com"
        cleaned = preprocessor.preprocess(test_text)
        
        print(f"Original: {test_text}")
        print(f"Cleaned:  {cleaned}")
        print("\n[SUCCESS] Preprocessing working!")
        return True
    except Exception as e:
        print(f"[FAIL] Preprocessing failed: {e}")
        print("\n[X] Preprocessing test failed!")
        return False


def test_vectorization():
    """Test feature extraction"""
    print("\n" + "="*70)
    print("TESTING FEATURE EXTRACTION")
    print("="*70)
    
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        
        documents = [
            "machine learning is great",
            "deep learning is powerful",
            "natural language processing"
        ]
        
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(documents)
        
        print(f"[OK] Vectorization successful")
        print(f"  - Shape: {X.shape}")
        print(f"  - Vocabulary size: {len(vectorizer.get_feature_names_out())}")
        print("\n[SUCCESS] Feature extraction working!")
        return True
    except Exception as e:
        print(f"[FAIL] Vectorization failed: {e}")
        print("\n[X] Feature extraction test failed!")
        return False


def test_model_training():
    """Test model training"""
    print("\n" + "="*70)
    print("TESTING MODEL TRAINING")
    print("="*70)
    
    try:
        from sklearn.naive_bayes import MultinomialNB
        from sklearn.feature_extraction.text import TfidfVectorizer
        import numpy as np
        
        # Sample data
        X_train = ["machine learning", "deep learning", "data science", "artificial intelligence"]
        y_train = [0, 0, 1, 1]
        
        # Vectorize
        vectorizer = TfidfVectorizer()
        X_train_vec = vectorizer.fit_transform(X_train)
        
        # Train
        model = MultinomialNB()
        model.fit(X_train_vec, y_train)
        
        # Predict
        X_test = ["machine learning is great"]
        X_test_vec = vectorizer.transform(X_test)
        prediction = model.predict(X_test_vec)
        
        print(f"[OK] Model trained successfully")
        print(f"  - Training samples: {len(X_train)}")
        print(f"  - Test prediction: {prediction[0]}")
        print("\n[SUCCESS] Model training working!")
        return True
    except Exception as e:
        print(f"[FAIL] Model training failed: {e}")
        print("\n[X] Model training test failed!")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("NEWS CLASSIFICATION PROJECT - SETUP VERIFICATION")
    print("="*70)
    print("\nThis script will verify that your environment is set up correctly.\n")
    
    results = []
    
    # Run tests
    results.append(("Library Imports", test_imports()))
    results.append(("NLTK Data", test_nltk_data()))
    results.append(("Dataset Access", test_sklearn_dataset()))
    results.append(("Text Preprocessing", test_preprocessing()))
    results.append(("Feature Extraction", test_vectorization()))
    results.append(("Model Training", test_model_training()))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{test_name:30s} - {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "="*70)
    if all_passed:
        print("ALL TESTS PASSED!")
        print("="*70)
        print("\nYou're ready to run the main project:")
        print("  python news_classification.py")
        print("\nOr open the Jupyter notebook:")
        print("  jupyter notebook news_classification.ipynb")
    else:
        print("SOME TESTS FAILED")
        print("="*70)
        print("\nPlease fix the issues above before running the main project.")
        print("\nCommon fixes:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Download NLTK data: python -c \"import nltk; nltk.download('all')\"")
        print("  3. Check internet connection for dataset download")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
