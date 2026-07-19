"""
Streamlit Web Application for News Topic Classification
Interactive UI for model training, evaluation, and predictions
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
import pickle
import os
from utils import TextPreprocessor, get_top_features
import time

# Page configuration
st.set_page_config(
    page_title="News Topic Classification",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-top: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_dataset():
    """Load 20 Newsgroups dataset"""
    train_data = fetch_20newsgroups(
        subset='train',
        shuffle=True,
        random_state=42,
        remove=('headers', 'footers', 'quotes')
    )
    test_data = fetch_20newsgroups(
        subset='test',
        shuffle=True,
        random_state=42,
        remove=('headers', 'footers', 'quotes')
    )
    return train_data, test_data


@st.cache_data
def preprocess_data(train_texts, test_texts):
    """Preprocess text data"""
    preprocessor = TextPreprocessor(use_lemmatization=True)
    X_train_clean = [preprocessor.preprocess(text) for text in train_texts]
    X_test_clean = [preprocessor.preprocess(text) for text in test_texts]
    return X_train_clean, X_test_clean


@st.cache_data
def extract_features(X_train, X_test, method='tfidf', max_features=5000):
    """Extract features using vectorization"""
    if method == 'count':
        vectorizer = CountVectorizer(max_features=max_features, ngram_range=(1, 2), min_df=2)
    else:
        vectorizer = TfidfVectorizer(max_features=max_features, ngram_range=(1, 2), min_df=2)
    
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    return X_train_vec, X_test_vec, vectorizer


@st.cache_resource
def train_model(X_train, y_train, model_name='svm'):
    """Train classification model"""
    if model_name == 'naive_bayes':
        model = MultinomialNB(alpha=0.1)
    elif model_name == 'logistic_regression':
        model = LogisticRegression(max_iter=1000, random_state=42, C=1.0)
    elif model_name == 'svm':
        model = LinearSVC(random_state=42, C=1.0, max_iter=2000)
    
    model.fit(X_train, y_train)
    return model


def plot_confusion_matrix(cm, categories):
    """Plot confusion matrix"""
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(cm, annot=False, fmt='d', cmap='Blues', 
                xticklabels=categories, yticklabels=categories,
                cbar_kws={'label': 'Count'}, ax=ax)
    ax.set_xlabel('Predicted Category', fontsize=12)
    ax.set_ylabel('True Category', fontsize=12)
    ax.set_title('Confusion Matrix', fontsize=14, fontweight='bold')
    plt.xticks(rotation=90, ha='right', fontsize=8)
    plt.yticks(rotation=0, fontsize=8)
    plt.tight_layout()
    return fig


def plot_model_comparison(results_df):
    """Plot model comparison"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
    
    # Accuracy
    ax1.bar(results_df['Model'], results_df['Accuracy'], color=colors[:len(results_df)])
    ax1.set_ylabel('Accuracy', fontsize=12)
    ax1.set_title('Model Accuracy Comparison', fontsize=14, fontweight='bold')
    ax1.set_ylim([0.7, 0.9])
    for i, v in enumerate(results_df['Accuracy']):
        ax1.text(i, v + 0.01, f'{v:.3f}', ha='center', fontweight='bold')
    
    # F1-Score
    ax2.bar(results_df['Model'], results_df['F1_Score'], color=colors[:len(results_df)])
    ax2.set_ylabel('F1-Score', fontsize=12)
    ax2.set_title('Model F1-Score Comparison', fontsize=14, fontweight='bold')
    ax2.set_ylim([0.7, 0.9])
    for i, v in enumerate(results_df['F1_Score']):
        ax2.text(i, v + 0.01, f'{v:.3f}', ha='center', fontweight='bold')
    
    plt.tight_layout()
    return fig


def main():
    # Header
    st.markdown('<h1 class="main-header">📰 News Topic Classification</h1>', unsafe_allow_html=True)
    st.markdown("### Using Natural Language Processing and Machine Learning")
    
    # Sidebar
    st.sidebar.title("⚙️ Configuration")
    page = st.sidebar.radio("Navigate", 
                            ["🏠 Home", "📊 Dataset Explorer", "🤖 Train Models", 
                             "🔮 Make Predictions", "📈 Model Comparison", "ℹ️ About"])
    
    # Initialize session state
    if 'trained_models' not in st.session_state:
        st.session_state.trained_models = {}
    if 'vectorizers' not in st.session_state:
        st.session_state.vectorizers = {}
    if 'results' not in st.session_state:
        st.session_state.results = []
    
    # HOME PAGE
    if page == "🏠 Home":
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🎯 Objective")
            st.write("""
            Automatically classify news articles into 20 different categories using 
            state-of-the-art NLP and machine learning techniques.
            """)
        
        with col2:
            st.markdown("### 📚 Dataset")
            st.write("""
            **20 Newsgroups Dataset**
            - ~18,000 documents
            - 20 categories
            - Real-world newsgroup posts
            """)
        
        with col3:
            st.markdown("### 🚀 Features")
            st.write("""
            - Interactive data exploration
            - Multiple ML models
            - Real-time predictions
            - Performance visualization
            """)
        
        st.markdown("---")
        st.markdown("### 🔑 Key Capabilities")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Text Processing:**
            - Preprocessing pipeline
            - TF-IDF vectorization
            - N-gram features
            
            **Models:**
            - Naive Bayes
            - Logistic Regression
            - Linear SVM
            """)
        
        with col2:
            st.markdown("""
            **Evaluation:**
            - Accuracy metrics
            - Confusion matrix
            - F1-Score analysis
            
            **Deployment:**
            - Real-time predictions
            - Interactive UI
            - Model comparison
            """)
        
        st.markdown("---")
        st.info("👈 Use the sidebar to navigate through different sections!")
    
    # DATASET EXPLORER
    elif page == "📊 Dataset Explorer":
        st.markdown('<h2 class="sub-header">📊 Dataset Explorer</h2>', unsafe_allow_html=True)
        
        with st.spinner("Loading dataset..."):
            train_data, test_data = load_dataset()
        
        st.success(f"✅ Dataset loaded successfully!")
        
        # Dataset statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Training Samples", len(train_data.data))
        with col2:
            st.metric("Test Samples", len(test_data.data))
        with col3:
            st.metric("Categories", len(train_data.target_names))
        
        # Categories
        st.markdown("### 📋 All Categories")
        categories_df = pd.DataFrame({
            'ID': range(1, len(train_data.target_names) + 1),
            'Category': train_data.target_names
        })
        st.dataframe(categories_df, use_container_width=True)
        
        # Category distribution
        st.markdown("### 📊 Category Distribution")
        train_df = pd.DataFrame({
            'category': [train_data.target_names[i] for i in train_data.target]
        })
        
        fig, ax = plt.subplots(figsize=(12, 6))
        train_df['category'].value_counts().plot(kind='barh', color='steelblue', ax=ax)
        ax.set_title('Distribution of Categories in Training Data', fontsize=14, fontweight='bold')
        ax.set_xlabel('Number of Documents')
        ax.set_ylabel('Category')
        plt.tight_layout()
        st.pyplot(fig)
        
        # Sample documents
        st.markdown("### 📄 Sample Documents")
        category_filter = st.selectbox("Select Category", train_data.target_names)
        
        # Get samples from selected category
        category_idx = train_data.target_names.index(category_filter)
        samples = [i for i, target in enumerate(train_data.target) if target == category_idx]
        
        if samples:
            sample_idx = st.slider("Sample Number", 0, min(len(samples)-1, 9), 0)
            st.text_area("Document Text", train_data.data[samples[sample_idx]], height=300)
    
    # TRAIN MODELS
    elif page == "🤖 Train Models":
        st.markdown('<h2 class="sub-header">🤖 Train Models</h2>', unsafe_allow_html=True)
        
        # Load data
        with st.spinner("Loading dataset..."):
            train_data, test_data = load_dataset()
        
        st.success("✅ Dataset loaded!")
        
        # Configuration
        st.markdown("### ⚙️ Training Configuration")
        col1, col2 = st.columns(2)
        
        with col1:
            vectorization_method = st.selectbox(
                "Feature Extraction Method",
                ["TF-IDF", "Bag-of-Words"],
                help="TF-IDF generally performs better"
            )
            max_features = st.slider("Max Features", 1000, 10000, 5000, 1000)
        
        with col2:
            model_type = st.selectbox(
                "Model Type",
                ["Linear SVM", "Logistic Regression", "Naive Bayes"]
            )
        
        # Train button
        if st.button("🚀 Train Model", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Preprocessing
            status_text.text("Step 1/4: Preprocessing text data...")
            progress_bar.progress(25)
            X_train_clean, X_test_clean = preprocess_data(train_data.data, test_data.data)
            time.sleep(0.5)
            
            # Feature extraction
            status_text.text("Step 2/4: Extracting features...")
            progress_bar.progress(50)
            method = 'tfidf' if vectorization_method == "TF-IDF" else 'count'
            X_train_vec, X_test_vec, vectorizer = extract_features(
                X_train_clean, X_test_clean, method, max_features
            )
            time.sleep(0.5)
            
            # Model training
            status_text.text("Step 3/4: Training model...")
            progress_bar.progress(75)
            model_map = {
                "Linear SVM": "svm",
                "Logistic Regression": "logistic_regression",
                "Naive Bayes": "naive_bayes"
            }
            model = train_model(X_train_vec, train_data.target, model_map[model_type])
            time.sleep(0.5)
            
            # Evaluation
            status_text.text("Step 4/4: Evaluating model...")
            progress_bar.progress(100)
            y_pred = model.predict(X_test_vec)
            accuracy = accuracy_score(test_data.target, y_pred)
            f1 = f1_score(test_data.target, y_pred, average='macro')
            
            # Save to session state
            model_key = f"{model_type}_{vectorization_method}"
            st.session_state.trained_models[model_key] = model
            st.session_state.vectorizers[model_key] = vectorizer
            st.session_state.results.append({
                'Model': model_key,
                'Accuracy': accuracy,
                'F1_Score': f1
            })
            
            status_text.empty()
            progress_bar.empty()
            
            # Results
            st.markdown("---")
            st.markdown("### 🎯 Training Results")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Accuracy", f"{accuracy:.4f}", f"{accuracy*100:.2f}%")
            with col2:
                st.metric("Macro F1-Score", f"{f1:.4f}")
            
            # Classification report
            st.markdown("### 📊 Classification Report")
            report = classification_report(test_data.target, y_pred, 
                                          target_names=train_data.target_names,
                                          output_dict=True)
            report_df = pd.DataFrame(report).transpose()
            st.dataframe(report_df.style.highlight_max(axis=0), use_container_width=True)
            
            # Confusion matrix
            st.markdown("### 🔍 Confusion Matrix")
            cm = confusion_matrix(test_data.target, y_pred)
            fig = plot_confusion_matrix(cm, train_data.target_names)
            st.pyplot(fig)
            
            st.success(f"✅ Model trained successfully! Accuracy: {accuracy*100:.2f}%")
    
    # MAKE PREDICTIONS
    elif page == "🔮 Make Predictions":
        st.markdown('<h2 class="sub-header">🔮 Make Predictions</h2>', unsafe_allow_html=True)
        
        if not st.session_state.trained_models:
            st.warning("⚠️ No trained models available. Please train a model first!")
            if st.button("Go to Train Models"):
                st.rerun()
        else:
            # Model selection
            model_key = st.selectbox("Select Model", list(st.session_state.trained_models.keys()))
            
            # Text input
            st.markdown("### 📝 Enter Text for Classification")
            user_text = st.text_area(
                "Input Text",
                placeholder="Enter news article text here...",
                height=200
            )
            
            # Sample texts
            st.markdown("### 📋 Or Try Sample Texts")
            samples = {
                "Space": "NASA launched a new Mars rover to explore the red planet surface and search for signs of ancient life",
                "Sports": "The baseball game was exciting with a home run in the final inning securing the championship victory",
                "Technology": "New graphics card released with improved performance for gaming and AI applications using advanced architecture",
                "Medicine": "Scientists discovered a new treatment for cancer using gene therapy and immunotherapy techniques",
                "Politics": "The government announced new policies on healthcare reform and economic stimulus packages"
            }
            
            sample_choice = st.selectbox("Select Sample", ["Custom"] + list(samples.keys()))
            if sample_choice != "Custom":
                user_text = samples[sample_choice]
                st.text_area("Selected Sample", user_text, height=100)
            
            # Predict button
            if st.button("🔮 Predict Category", type="primary"):
                if user_text.strip():
                    with st.spinner("Analyzing text..."):
                        # Preprocess
                        preprocessor = TextPreprocessor(use_lemmatization=True)
                        cleaned_text = preprocessor.preprocess(user_text)
                        
                        # Vectorize
                        vectorizer = st.session_state.vectorizers[model_key]
                        text_vec = vectorizer.transform([cleaned_text])
                        
                        # Predict
                        model = st.session_state.trained_models[model_key]
                        prediction = model.predict(text_vec)[0]
                        
                        # Get confidence scores
                        train_data, _ = load_dataset()
                        predicted_category = train_data.target_names[prediction]
                        
                        # Display results
                        st.markdown("---")
                        st.markdown("### 🎯 Prediction Results")
                        
                        st.success(f"**Predicted Category:** {predicted_category}")
                        
                        # Get top predictions if available
                        if hasattr(model, 'decision_function'):
                            scores = model.decision_function(text_vec)[0]
                            top_3_idx = scores.argsort()[-3:][::-1]
                            
                            st.markdown("### 📊 Top 3 Predictions")
                            for i, idx in enumerate(top_3_idx, 1):
                                st.write(f"{i}. **{train_data.target_names[idx]}** (Score: {scores[idx]:.4f})")
                        
                        # Show preprocessing
                        with st.expander("🔍 View Preprocessing Details"):
                            st.write("**Original Text:**")
                            st.write(user_text[:200] + "..." if len(user_text) > 200 else user_text)
                            st.write("**Preprocessed Text:**")
                            st.write(cleaned_text[:200] + "..." if len(cleaned_text) > 200 else cleaned_text)
                else:
                    st.error("❌ Please enter some text!")
    
    # MODEL COMPARISON
    elif page == "📈 Model Comparison":
        st.markdown('<h2 class="sub-header">📈 Model Comparison</h2>', unsafe_allow_html=True)
        
        if not st.session_state.results:
            st.warning("⚠️ No models trained yet. Train some models to see comparison!")
        else:
            results_df = pd.DataFrame(st.session_state.results)
            
            # Display table
            st.markdown("### 📊 Performance Metrics")
            st.dataframe(results_df.style.highlight_max(axis=0), use_container_width=True)
            
            # Plot comparison
            st.markdown("### 📈 Visual Comparison")
            fig = plot_model_comparison(results_df)
            st.pyplot(fig)
            
            # Best model
            best_model = results_df.loc[results_df['Accuracy'].idxmax()]
            st.markdown("### 🏆 Best Model")
            st.success(f"**{best_model['Model']}** with accuracy of **{best_model['Accuracy']:.4f}**")
            
            # Clear results
            if st.button("🗑️ Clear All Results"):
                st.session_state.results = []
                st.session_state.trained_models = {}
                st.session_state.vectorizers = {}
                st.rerun()
    
    # ABOUT
    elif page == "ℹ️ About":
        st.markdown('<h2 class="sub-header">ℹ️ About This Project</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        ### 📰 News Topic Classification using NLP
        
        This project demonstrates a complete Natural Language Processing pipeline for 
        automatically classifying news articles into 20 different categories.
        
        #### 🎯 Key Features:
        - **Text Preprocessing**: Cleaning, tokenization, lemmatization
        - **Feature Extraction**: TF-IDF and Bag-of-Words
        - **Multiple Models**: Naive Bayes, Logistic Regression, Linear SVM
        - **Interactive UI**: Built with Streamlit
        - **Real-time Predictions**: Classify custom text instantly
        
        #### 📊 Dataset:
        **20 Newsgroups Dataset** - A collection of approximately 18,000 newsgroup documents, 
        partitioned across 20 different newsgroups.
        
        #### 🛠️ Technologies:
        - Python 3.8+
        - scikit-learn
        - NLTK
        - Streamlit
        - pandas, numpy
        - matplotlib, seaborn
        
        #### 🎓 Educational Purpose:
        This project is designed for Data Science and Big Data Analytics coursework, 
        demonstrating practical NLP and machine learning skills.
        
        #### 📈 Expected Performance:
        - Naive Bayes: ~77-82% accuracy
        - Logistic Regression: ~85% accuracy
        - Linear SVM: ~86% accuracy
        
        #### 🌍 Real-World Applications:
        - News aggregation (Google News)
        - Email filtering (Gmail)
        - Customer support automation
        - Content moderation
        - Market research
        
        ---
        
        **Created by:** Your Name  
        **Course:** Data Science and Big Data Analytics  
        **Year:** 2024
        """)
        
        st.markdown("---")
        st.info("💡 **Tip:** Navigate through different sections using the sidebar!")


if __name__ == "__main__":
    main()
