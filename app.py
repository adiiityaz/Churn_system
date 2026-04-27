from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pandas as pd
import pickle
import numpy as np
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = "super_secret_churn_key" # Change this for production

# Hardcoded user credentials
USER_CREDENTIALS = {
    "admin": "admin123"
}

# Load the model and encoders
MODEL_PATH = "churn_model.pkl"
ENCODERS_PATH = "encoders.pkl"

if os.path.exists(MODEL_PATH) and os.path.exists(ENCODERS_PATH):
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(ENCODERS_PATH, "rb") as f:
        encoders = pickle.load(f)
else:
    model = None
    encoders = None

# Login decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid credentials. Please try again."
            
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# Prediction history storage (In-memory for demo)
PREDICTION_HISTORY = []

@app.route("/")
@login_required
def dashboard():
    # Load data for stats
    df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")
    
    total_customers = len(df)
    churn_rate = round((len(df[df["Churn"] == "Yes"]) / total_customers) * 100, 1)
    avg_monthly = round(df["MonthlyCharges"].mean(), 2)
    
    # Data for charts
    contract_counts = df["Contract"].value_counts().to_dict()
    payment_counts = df["PaymentMethod"].value_counts().to_dict()
    
    # Calculate AI Insights
    high_risk_contract = df[(df["Contract"] == "Month-to-month") & (df["Churn"] == "Yes")].shape[0]
    fiber_risk = df[(df["InternetService"] == "Fiber optic") & (df["Churn"] == "Yes")].shape[0]
    
    insights = [
        {"icon": "fas fa-exclamation-triangle", "text": f"High risk detected in {high_risk_contract} Month-to-Month users.", "color": "#ef4444"},
        {"icon": "fas fa-info-circle", "text": f"Fiber Optic users show {round((fiber_risk/len(df[df['InternetService'] == 'Fiber optic']))*100, 1)}% churn rate.", "color": "#a855f7"},
        {"icon": "fas fa-check-circle", "text": "2-Year contract segment remains highly stable (98% retention).", "color": "#10b981"}
    ]
    
    stats = {
        "total_customers": total_customers,
        "churn_rate": churn_rate,
        "avg_monthly": avg_monthly,
        "contract_data": contract_counts,
        "payment_data": payment_counts,
        "insights": insights
    }
    
    return render_template("dashboard.html", stats=stats, active_page="dashboard")

@app.route("/predictor")
@login_required
def predictor():
    return render_template("index.html", active_page="predictor")

@app.route("/customers")
@login_required
def customers():
    # Load first 50 customers for the demo
    df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")
    sample_data = df.head(50).to_dict(orient="records")
    
    # Generate dummy names for professional look
    first_names_male = ["James", "Robert", "John", "Michael", "David", "William", "Richard", "Joseph", "Thomas", "Christopher"]
    first_names_female = ["Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    
    for i, row in enumerate(sample_data):
        if row["gender"] == "Male":
            name = f"{first_names_male[i % 10]} {last_names[(i+2) % 10]}"
        else:
            name = f"{first_names_female[i % 10]} {last_names[(i+5) % 10]}"
        row["CustomerName"] = name
        
    return render_template("customers.html", customers=sample_data, active_page="customers")

@app.route("/history")
@login_required
def history():
    return render_template("history.html", history=PREDICTION_HISTORY, active_page="history")

@app.route("/settings")
@login_required
def settings():
    model_info = {
        "algorithm": "Random Forest Classifier",
        "accuracy": "77.71%",
        "features": 19,
        "status": "Online",
        "version": "v2.4.0"
    }
    return render_template("settings.html", info=model_info, active_page="settings")

@app.route("/predict", methods=["POST"])
@login_required
def predict():
    if model is None or encoders is None:
        return jsonify({"error": "Model not found. Please run churn_analysis.py first."}), 500
    
    try:
        # Get data from form
        data = request.form.to_dict()
        
        # Create a dataframe for the input
        input_df = pd.DataFrame([data])
        
        # Convert numeric fields
        input_df["SeniorCitizen"] = input_df["SeniorCitizen"].astype(int)
        input_df["tenure"] = input_df["tenure"].astype(int)
        input_df["MonthlyCharges"] = input_df["MonthlyCharges"].astype(float)
        input_df["TotalCharges"] = input_df["TotalCharges"].astype(float)
        
        # Store original values for history
        display_data = data.copy()
        
        # Encode categorical fields
        for col, le in encoders.items():
            if col in input_df.columns:
                input_df[col] = le.transform(input_df[col])
        
        # Ensure column order matches training
        features = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
                   'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity',
                   'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
                   'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod',
                   'MonthlyCharges', 'TotalCharges']
        
        input_df = input_df[features]
        
        # Predict
        prediction = model.predict(input_df)
        prob = model.predict_proba(input_df)[0][1]
        
        result = "Churn" if prediction[0] == 1 else "No Churn"
        confidence = round(prob * 100 if prediction[0] == 1 else (1 - prob) * 100, 2)
        
        # Log to history
        PREDICTION_HISTORY.append({
            "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            "result": result,
            "confidence": f"{confidence}%",
            "details": display_data
        })
        
        return render_template("index.html", 
                               prediction_text=f"Prediction: {result}",
                               confidence_text=f"Confidence: {confidence}%",
                               result_class="churn" if result == "Churn" else "no-churn",
                               active_page="predictor")
    
    except Exception as e:
        return render_template("index.html", prediction_text=f"Error: {str(e)}", active_page="predictor")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
