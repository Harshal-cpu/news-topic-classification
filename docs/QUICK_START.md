# 🚀 Quick Start Guide

## Step-by-Step Instructions to Run the Project

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- 2GB free disk space
- Internet connection (for downloading dataset)

---

## 📥 Installation

### Step 1: Navigate to Project Directory
```bash
cd "c:\Users\Harsh\OneDrive\Desktop\dsbda mini project"
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download NLTK Data
```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
```

---

## 🏃 Running the Project

### Option 1: Run Python Script (Recommended for First Time)
```bash
python news_classification.py
```

**What it does**:
- Loads 20 Newsgroups dataset
- Preprocesses text data
- Trains 4 different models
- Generates evaluation metrics
- Creates visualizations in `outputs/` folder
- Shows sample predictions

**Expected Runtime**: 5-10 minutes

**Output**:
- Console output with metrics
- `outputs/confusion_matrix_*.png` - Confusion matrices
- `outputs/model_comparison.png` - Model comparison chart

---

### Option 2: Run Jupyter Notebook (Interactive)
```bash
# Install Jupyter if not already installed
pip install jupyter

# Start Jupyter
jupyter notebook

# Open: news_classification.ipynb
```

**Advantages**:
- Step-by-step execution
- See intermediate results
- Modify and experiment
- Better for learning

---

### Option 3: Run Flask API (For Deployment)
```bash
python api.py
```

**API will start at**: http://localhost:5000

**Test the API**:

#### Using curl (Command Line):
```bash
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d "{\"text\":\"NASA launched a new satellite to study climate change\"}"
```

#### Using Python:
```python
import requests

response = requests.post(
    'http://localhost:5000/predict',
    json={'text': 'NASA launched a new satellite'}
)
print(response.json())
```

#### Using Postman:
1. Method: POST
2. URL: http://localhost:5000/predict
3. Headers: Content-Type: application/json
4. Body (raw JSON):
```json
{
    "text": "NASA launched a new satellite"
}
```

---

## 📊 Expected Results

### Model Performance
| Model | Accuracy | F1-Score |
|-------|----------|----------|
| Naive Bayes + Count | ~77% | ~0.75 |
| Naive Bayes + TF-IDF | ~82% | ~0.80 |
| Logistic Regression + TF-IDF | ~85% | ~0.84 |
| **Linear SVM + TF-IDF** | **~86%** | **~0.85** |

### Sample Predictions
```
Input: "NASA launched a new Mars rover"
Predicted: sci.space

Input: "The baseball game was exciting"
Predicted: rec.sport.baseball

Input: "New graphics card released"
Predicted: comp.graphics
```

---

## 📁 Project Structure After Running

```
dsbda-mini-project/
│
├── requirements.txt              # Dependencies
├── README.md                     # Project documentation
├── CONCEPTS_AND_VIVA.md         # Viva preparation
├── QUICK_START.md               # This file
│
├── news_classification.py        # Main script
├── news_classification.ipynb     # Jupyter notebook
├── api.py                        # Flask API
├── utils.py                      # Helper functions
│
├── outputs/                      # Generated files
│   ├── confusion_matrix_naive_bayes_count.png
│   ├── confusion_matrix_naive_bayes_tfidf.png
│   ├── confusion_matrix_logistic_regression.png
│   ├── confusion_matrix_svm.png
│   └── model_comparison.png
│
├── models/                       # Saved models (after API run)
│   ├── model.pkl
│   ├── vectorizer.pkl
│   └── categories.pkl
│
└── venv/                         # Virtual environment
```

---

## 🐛 Troubleshooting

### Issue 1: Module Not Found Error
```
ModuleNotFoundError: No module named 'sklearn'
```
**Solution**:
```bash
pip install scikit-learn
```

### Issue 2: NLTK Data Not Found
```
LookupError: Resource stopwords not found
```
**Solution**:
```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
```

### Issue 3: Memory Error
```
MemoryError: Unable to allocate array
```
**Solution**: Reduce max_features in vectorizers
```python
# In news_classification.py, change:
max_features=5000  # to
max_features=3000
```

### Issue 4: Slow Execution
**Solution**: 
- Use smaller subset of data for testing
- Reduce max_iter in models
- Skip some models initially

### Issue 5: Port Already in Use (API)
```
OSError: [Errno 48] Address already in use
```
**Solution**:
```bash
# Change port in api.py
app.run(port=5001)  # Instead of 5000
```

---

## 🎯 What to Present in Viva

### 1. Run the Main Script
```bash
python news_classification.py
```
Show the output and explain each step.

### 2. Show Visualizations
Open files in `outputs/` folder and explain:
- Confusion matrix interpretation
- Model comparison results
- Which categories are confused and why

### 3. Demonstrate API
```bash
python api.py
```
Make a prediction and show JSON response.

### 4. Show Jupyter Notebook
Open notebook and explain:
- Preprocessing steps
- Feature extraction
- Model training
- Evaluation metrics

### 5. Explain Code
Be ready to explain:
- `utils.py` - Preprocessing functions
- `news_classification.py` - Main pipeline
- `api.py` - REST API implementation

---

## 📝 Customization

### Change Dataset Size
```python
# In news_classification.py
train_data = fetch_20newsgroups(
    subset='train',
    categories=['comp.graphics', 'sci.space']  # Only 2 categories
)
```

### Add New Model
```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=100)
rf.fit(X_train_tfidf, y_train)
```

### Modify Preprocessing
```python
# In utils.py, modify TextPreprocessor class
def clean_text(self, text):
    # Add your custom preprocessing
    text = text.lower()
    # ... more steps
    return text
```

---

## 🎓 Learning Path

### Beginner
1. Run `news_classification.py`
2. Understand output
3. Read `CONCEPTS_AND_VIVA.md`

### Intermediate
1. Open Jupyter notebook
2. Run cell by cell
3. Modify parameters
4. Experiment with different models

### Advanced
1. Add new features (document length, special chars)
2. Implement cross-validation
3. Try deep learning (LSTM, BERT)
4. Scale with PySpark

---

## 📞 Support

### Common Questions

**Q: How long does it take to run?**
A: 5-10 minutes for full script, depending on your machine.

**Q: Can I use a subset of categories?**
A: Yes, modify the `fetch_20newsgroups()` call with `categories` parameter.

**Q: How do I save the trained model?**
A: Run `api.py` - it automatically saves models in `models/` folder.

**Q: Can I use this for other text classification tasks?**
A: Yes! Just replace the dataset and adjust preprocessing.

---

## ✅ Checklist Before Viva

- [ ] All dependencies installed
- [ ] Script runs without errors
- [ ] Visualizations generated in `outputs/`
- [ ] Understand TF-IDF concept
- [ ] Can explain preprocessing steps
- [ ] Know why SVM performed best
- [ ] Can demonstrate API
- [ ] Read `CONCEPTS_AND_VIVA.md`
- [ ] Prepared to explain code
- [ ] Know real-world applications

---

## 🎉 Success Indicators

You're ready when you can:
1. ✅ Run the script successfully
2. ✅ Explain each preprocessing step
3. ✅ Interpret confusion matrix
4. ✅ Compare model performances
5. ✅ Make custom predictions
6. ✅ Explain TF-IDF vs Bag-of-Words
7. ✅ Demonstrate REST API
8. ✅ Discuss real-world applications

---

**Good luck with your project! 🚀**

For detailed concepts, see: `CONCEPTS_AND_VIVA.md`
For project overview, see: `README.md`
