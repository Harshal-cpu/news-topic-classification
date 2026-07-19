# 🎨 Streamlit Web Application Guide

## Overview

A beautiful, interactive web interface for the News Topic Classification project built with Streamlit.

## Features

### 🏠 Home Page
- Project overview
- Key capabilities
- Quick navigation

### 📊 Dataset Explorer
- View dataset statistics
- Explore all 20 categories
- Visualize category distribution
- Browse sample documents

### 🤖 Train Models
- Configure training parameters
- Choose feature extraction method (TF-IDF or Bag-of-Words)
- Select model type (SVM, Logistic Regression, Naive Bayes)
- View training progress
- See detailed results and metrics
- Visualize confusion matrix

### 🔮 Make Predictions
- Classify custom text
- Try pre-loaded sample texts
- See top 3 predictions
- View preprocessing details
- Real-time results

### 📈 Model Comparison
- Compare multiple trained models
- View performance metrics table
- Visual comparison charts
- Identify best performing model

### ℹ️ About
- Project information
- Technologies used
- Real-world applications

## Installation

The Streamlit package is already included in your requirements.txt. If you need to install it separately:

```bash
pip install streamlit
```

## Running the Application

### Method 1: Command Line
```bash
streamlit run streamlit_app.py
```

### Method 2: Using Batch File (Windows)
Update `run_project.bat` to include Streamlit option (see below).

### Method 3: Direct Python
```bash
python -m streamlit run streamlit_app.py
```

## What Happens When You Run

1. **Browser Opens Automatically** - Streamlit will open your default browser
2. **Local URL** - Application runs at `http://localhost:8501`
3. **Interactive Interface** - Navigate using the sidebar

## Usage Guide

### Step 1: Explore Dataset
1. Click "📊 Dataset Explorer" in sidebar
2. View statistics and categories
3. Browse sample documents

### Step 2: Train a Model
1. Click "🤖 Train Models"
2. Select feature extraction method (TF-IDF recommended)
3. Choose model type (Linear SVM recommended)
4. Click "🚀 Train Model"
5. Wait for training to complete (~2-5 minutes)
6. View results and confusion matrix

### Step 3: Make Predictions
1. Click "🔮 Make Predictions"
2. Select your trained model
3. Enter custom text OR select a sample
4. Click "🔮 Predict Category"
5. View predicted category and confidence scores

### Step 4: Compare Models
1. Train multiple models with different configurations
2. Click "📈 Model Comparison"
3. View comparison table and charts
4. Identify best performing model

## Features Highlights

### Interactive Training
- Real-time progress bar
- Step-by-step status updates
- Immediate results display

### Visual Analytics
- Confusion matrix heatmap
- Model comparison charts
- Category distribution plots

### User-Friendly
- Clean, modern interface
- Intuitive navigation
- Helpful tooltips
- Sample texts provided

### Performance
- Caching for faster loading
- Efficient data handling
- Smooth user experience

## Tips for Best Experience

### 1. Start with Dataset Explorer
Get familiar with the data before training models.

### 2. Use TF-IDF
Generally performs better than Bag-of-Words.

### 3. Try Different Models
Train multiple models to compare performance.

### 4. Test with Samples
Use provided sample texts to quickly test predictions.

### 5. Adjust Max Features
Experiment with different vocabulary sizes (1000-10000).

## Keyboard Shortcuts

- **Ctrl + R** - Rerun the app
- **Ctrl + C** - Stop the server (in terminal)

## Troubleshooting

### Issue: Port Already in Use
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Issue: Browser Doesn't Open
Manually navigate to: `http://localhost:8501`

### Issue: Slow Training
- Reduce max_features to 3000
- Use smaller dataset subset
- This is normal for first run

### Issue: Model Not Found
Train a model first before making predictions.

## Advanced Configuration

### Change Port
```bash
streamlit run streamlit_app.py --server.port 8080
```

### Disable Auto-Open Browser
```bash
streamlit run streamlit_app.py --server.headless true
```

### Custom Theme
Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

## Screenshots Description

### Home Page
- Welcome message
- Project overview
- Key features
- Navigation guide

### Dataset Explorer
- Statistics cards
- Category list
- Distribution chart
- Sample document viewer

### Train Models
- Configuration panel
- Progress indicator
- Results metrics
- Confusion matrix

### Make Predictions
- Text input area
- Sample selector
- Prediction results
- Confidence scores

### Model Comparison
- Performance table
- Comparison charts
- Best model highlight

## Performance Metrics

### Expected Training Time
- Naive Bayes: ~1-2 minutes
- Logistic Regression: ~2-3 minutes
- Linear SVM: ~3-5 minutes

### Expected Accuracy
- Naive Bayes + TF-IDF: ~82%
- Logistic Regression + TF-IDF: ~85%
- Linear SVM + TF-IDF: ~86%

## Deployment Options

### Local Development
```bash
streamlit run streamlit_app.py
```

### Streamlit Cloud (Free)
1. Push code to GitHub
2. Go to share.streamlit.io
3. Connect repository
4. Deploy!

### Docker
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

## Comparison: Streamlit vs Flask API

| Feature | Streamlit | Flask API |
|---------|-----------|-----------|
| **UI** | Built-in, beautiful | Need to build |
| **Interactivity** | High | Low |
| **Setup** | Very easy | Moderate |
| **Use Case** | Demo, exploration | Production API |
| **Learning Curve** | Easy | Moderate |

## Why Streamlit?

### Advantages
✅ **Rapid Development** - Build UI in minutes  
✅ **No HTML/CSS/JS** - Pure Python  
✅ **Interactive Widgets** - Built-in components  
✅ **Auto-Refresh** - Changes reflect immediately  
✅ **Beautiful Design** - Professional look out-of-box  
✅ **Easy Deployment** - Free hosting on Streamlit Cloud  

### Best For
- Demos and presentations
- Data exploration
- Prototyping
- Educational projects
- Internal tools

## Integration with Existing Project

The Streamlit app integrates seamlessly with your existing code:
- Uses `utils.py` for preprocessing
- Leverages same models and vectorizers
- Compatible with all existing functions
- No changes needed to other files

## Next Steps

### After Running Streamlit App
1. ✅ Explore the dataset
2. ✅ Train multiple models
3. ✅ Make predictions
4. ✅ Compare performance
5. ✅ Show in presentation!

### For Viva/Demo
1. Open Streamlit app
2. Navigate through sections
3. Train a model live
4. Make predictions
5. Show comparison charts

## Stopping the Application

### In Terminal
Press `Ctrl + C`

### Confirmation
Type `y` when prompted

## Restarting

Simply run the command again:
```bash
streamlit run streamlit_app.py
```

## Additional Resources

### Streamlit Documentation
https://docs.streamlit.io

### Streamlit Gallery
https://streamlit.io/gallery

### Streamlit Community
https://discuss.streamlit.io

---

## Quick Command Reference

```bash
# Run app
streamlit run streamlit_app.py

# Run on different port
streamlit run streamlit_app.py --server.port 8080

# Run without opening browser
streamlit run streamlit_app.py --server.headless true

# Clear cache
streamlit cache clear

# Show version
streamlit version
```

---

**Status**: ✅ Ready to Run  
**Difficulty**: ⭐ Easy  
**Time to Setup**: 1 minute  
**Wow Factor**: 🚀 High!

**Perfect for presentations and demos! 🎉**
