# 🚀 ChurnAI: Customer Retention System

An end-to-end AI-driven solution designed to predict and visualize customer attrition for telecommunications providers. This system features a robust machine learning pipeline and a premium, executive-grade dashboard for real-time analytics and inference.

## 📋 Table of Contents
- [Executive Dashboard](#-executive-dashboard)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Installation & Setup](#-installation--setup)
- [Model Architecture](#-model-architecture)
- [Project Structure](#-project-structure)

## 📊 Executive Dashboard
The system provides a high-end web interface featuring:
- **Real-time Analytics**: Interactive charts for contract distribution and payment methods.
- **AI Strategic Insights**: Automated alerts for high-risk customer segments (e.g., Fiber Optic users).
- **Customer Database**: A searchable directory of 7,000+ customer records with instant churn status visibility.
- **Inference History**: Audit log of all AI predictions and confidence scores.

## ✨ Key Features
- **Modern UI/UX**: Premium dark-mode interface built with Vanilla CSS and Outfit typography.
- **SMOTE Balancing**: Handles class imbalance to ensure high recall for churners.
- **Enterprise Security**: Role-based access control with secure login session management.
- **Real-time Scoring**: Instant inference with probabilistic confidence circles.

## 💻 Technology Stack
- **Backend**: Python / Flask
- **Data Science**: Scikit-Learn, Pandas, NumPy, Imbalanced-Learn (SMOTE)
- **Frontend**: HTML5, Vanilla CSS, Chart.js, FontAwesome

## 🛠️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/adiiityaz/Churn_system.git
   cd Churn_system
   ```

2. **Install dependencies**:
   ```bash
   pip install pandas scikit-learn imbalanced-learn Flask matplotlib seaborn
   ```

3. **Train the AI Model**:
   Generate the latest model and encoders from the Telco dataset:
   ```bash
   python churn_analysis.py
   ```

4. **Launch the Portal**:
   ```bash
   python app.py
   ```
   Access at `http://127.0.0.1:5000`

### 🔑 Demo Credentials
- **Username**: `admin`
- **Password**: `admin123`

## 📈 Model Architecture
The system utilizes a **Random Forest Classifier** optimized for the Telco dataset:
- **Accuracy**: ~78%
- **Preprocessing**: Label Encoding for categorical features, TotalCharges cleanup.
- **Handling Imbalance**: SMOTE (Synthetic Minority Over-sampling Technique) applied during training.

## 📂 Project Structure
```text
├── WA_Fn-UseC_-Telco-Customer-Churn.csv  # Dataset
├── churn_analysis.py                      # Model training & pipeline
├── app.py                                 # Flask server & logic
├── templates/                             # UI Components
│   ├── dashboard.html                     # Analytics view
│   ├── index.html                         # Predictor interface
│   ├── customers.html                     # Searchable database
│   ├── history.html                       # Inference logs
│   ├── login.html                         # Access portal
│   └── settings.html                      # System info
├── .gitignore                             # Environment protection
└── README.md                              # Documentation
```

---
*Developed as a high-performance customer analytics solution.*
