# 🚀 Telco Customer Churn Prediction System

An end-to-end machine learning solution designed to predict customer attrition (churn) for telecommunications providers. This project features a robust data science pipeline and a modern, high-performance web interface for real-time inference.

## 📋 Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Model Performance](#model-performance)
- [Project Structure](#project-structure)

## 🔍 Overview
Predicting customer churn is critical for the telecommunications industry to improve retention strategies and customer lifetime value. This system analyzes historical customer behavior—including service usage, contract types, and demographics—to identify high-risk accounts before they leave.

## ✨ Key Features
- **End-to-End Pipeline**: Handles everything from raw data ingestion to model deployment.
- **SMOTE Balancing**: Implements Synthetic Minority Oversampling Technique (SMOTE) to handle class imbalance in churn data.
- **Modern Web UI**: A premium, dark-mode web interface built with Flask and modern CSS for intuitive user interaction.
- **Persistence**: Pre-trained models and encoders are serialized using Pickle for instant loading and inference.
- **Real-time Scoring**: Provides both churn prediction and a confidence probability score for every input.

## 💻 Technology Stack
- **Languages**: Python, HTML5, CSS3
- **Frameworks**: Flask (Web Backend)
- **Data Science**: 
  - Pandas & NumPy (Processing)
  - Scikit-learn (Modelling & Evaluation)
  - Imbalanced-learn (SMOTE)
  - XGBoost & Random Forest (Ensemble Learning)

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd "Churn _system"
   ```

2. **Install dependencies**:
   ```bash
   pip install pandas scikit-learn imbalanced-learn Flask xgboost matplotlib seaborn
   ```

## 🚀 Usage

### 1. Training the Model
Run the analysis script to process the data, train the model, and generate the necessary serialized files (`.pkl`):
```bash
python churn_analysis.py
```

### 2. Launching the Web Interface
Start the Flask web server to access the graphical predictor:
```bash
python app.py
```
Visit `http://127.0.0.1:5000` in your web browser.

## 📈 Model Performance
The current production model uses a **Random Forest Classifier** with the following metrics:
- **Overall Accuracy**: ~78%
- **Class Balancing**: SMOTE applied for improved recall on churners.
- **Optimization**: Hyperparameter tuning performed via cross-validation.

## 📂 Project Structure
```text
├── WA_Fn-UseC_-Telco-Customer-Churn.csv  # Dataset
├── Customer_Churn_Prediction_using_ML.ipynb # Research Notebook
├── churn_analysis.py                      # Main training script
├── app.py                                 # Flask application
├── templates/                             # Web UI components
│   └── index.html                         # Main interface
├── churn_model.pkl                        # Serialized model (auto-generated)
├── encoders.pkl                           # Serialized encoders (auto-generated)
└── README.md                              # Documentation
```

---
*Developed as a high-performance customer analytics solution.*
