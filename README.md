# News Topic Classification using NLP

## 📌 Project Overview
This project implements a complete Natural Language Processing (NLP) pipeline to classify news articles into 20 different categories using the famous 20 Newsgroups dataset. The project demonstrates text preprocessing, feature extraction, machine learning model training, and evaluation.

## 🎯 Objectives
- Build an end-to-end text classification system
- Compare different feature extraction techniques (Bag-of-Words vs TF-IDF)
- Evaluate multiple classification algorithms
- Provide insights into model performance and feature importance

## 📊 Dataset
**20 Newsgroups Dataset** (~18,000 documents)
- 20 different categories (topics)
- Real-world newsgroup posts
- Multi-class classification problem

### Categories Include:
- Computer Technology (comp.*)
- Recreation (rec.*)
- Science (sci.*)
- Politics & Religion (talk.*)
- For Sale (misc.forsale)

## 🛠️ Tech Stack
- **Python 3.8+**
- **scikit-learn**: Machine learning models and dataset
- **NLTK**: Text preprocessing
- **pandas & numpy**: Data manipulation
- **matplotlib & seaborn**: Visualization
- **Flask**: REST API (optional)

## 📁 Project Structure
```
dsbda-mini-project/
│
├── README.md                     # Project documentation
├── START_HERE.md                 # Quick start guide
├── requirements.txt              # Dependencies
├── run_project.bat               # Windows menu script
│
├── news_classification.py        # Main implementation
├── news_classification.ipynb     # Jupyter notebook
├── utils.py                      # Helper functions
├── test_setup.py                 # Setup verification
│
├── api.py                        # Flask REST API
├── streamlit_app.py              # Streamlit demo app
├── app.py                        # Production web app
│
├── TECHNICAL_DOCUMENTATION.md    # Complete technical guide
├── PRESENTATION_OUTLINE.md       # Presentation guide
│
├── models/                       # Saved ML models
├── outputs/                      # Generated visualizations
└── docs/                         # Additional documentation
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Download NLTK Data
```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet'); nltk.download('omw-1.4')"
```

### 3. Verify Setup
```bash
python test_setup.py
```

## 💻 Usage

### Option 1: Run Main Script
```bash
python news_classification.py
```

### Option 2: Run Jupyter Notebook
```bash
jupyter notebook news_classification.ipynb
```

### Option 3: Start Flask API
```bash
python api.py
```

### Option 4: Start Streamlit Demo
```bash
streamlit run streamlit_app.py
```

### Option 5: Start Production Web App (Recommended)
```bash
streamlit run app.py
```

### Option 6: Windows Menu (All Options)
```bash
run_project.bat
```

## 📈 Results

### Model Performance
| Model | Accuracy | Macro F1-Score |
|-------|----------|----------------|
| Naive Bayes (CountVectorizer) | ~77% | ~0.75 |
| Naive Bayes (TF-IDF) | ~82% | ~0.80 |
| Logistic Regression (TF-IDF) | ~85% | ~0.84 |
| Linear SVM (TF-IDF) | ~86% | ~0.85 |

### Key Insights
- TF-IDF outperforms simple Bag-of-Words
- Linear SVM achieves best performance
- Some categories are easily confused (e.g., comp.sys.* categories)

## 📚 Documentation

### Essential Docs (Root Directory)
- **README.md** - Project overview (this file)
- **START_HERE.md** - Quick start guide for beginners
- **TECHNICAL_DOCUMENTATION.md** - Complete technical explanation
- **PRESENTATION_OUTLINE.md** - Presentation guide for teachers

### Additional Docs (docs/ folder)
- **CONCEPTS_AND_VIVA.md** - Viva preparation with Q&A
- **QUICK_START.md** - Detailed setup instructions
- **USER_GUIDE.md** - End-user guide for web app
- **PRESENTATION_GUIDE.md** - Advanced presentation tips
- And more...

### Quick Links
- 🎯 **New to project?** Read `START_HERE.md`
- 📚 **Technical details?** Read `TECHNICAL_DOCUMENTATION.md`
- 🎤 **Preparing presentation?** Read `PRESENTATION_OUTLINE.md`
- 👥 **End user?** Read `docs/USER_GUIDE.md`

## 🌍 Real-World Applications
1. **News Aggregation**: Auto-categorize articles (Google News, Flipboard)
2. **Email Filtering**: Spam detection, priority inbox
3. **Customer Support**: Route tickets to correct department
4. **Content Moderation**: Flag inappropriate content
5. **Market Research**: Analyze customer feedback by topic

## 🔧 Extensions & Improvements
- ✅ Multiple classifiers (Naive Bayes, Logistic Regression, SVM)
- ✅ N-gram features (bigrams, trigrams)
- ✅ Feature importance analysis
- ✅ REST API for predictions
- 🔄 Deep Learning (LSTM, BERT) - Future work
- 🔄 PySpark for big data scaling - Future work

## 📚 Learning Outcomes
- Text preprocessing pipeline
- Feature engineering for NLP
- Multi-class classification
- Model evaluation and comparison
- Deployment basics (REST API)

## 👨‍💻 Author
**Your Name**  
Data Science and Big Data Analytics Mini Project

## 📝 License
Educational Project - Free to use and modify

## 🙏 Acknowledgments
- 20 Newsgroups Dataset by Ken Lang
- scikit-learn documentation
- NLTK community

---
**Note**: This project is designed for educational purposes and demonstrates fundamental NLP and machine learning concepts.
