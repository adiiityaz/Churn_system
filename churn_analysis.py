import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pickle
import os

# Set file paths
csv_path = r"f:\Churn _system\WA_Fn-UseC_-Telco-Customer-Churn.csv"

def run_analysis():
    print("--- Step 1: Loading Data ---")
    if not os.path.exists(csv_path):
        print(f"Error: Dataset not found at {csv_path}")
        return

    df = pd.read_csv(csv_path)
    print(f"Dataset Shape: {df.shape}")
    
    print("\n--- Step 2: Data Cleaning ---")
    # Dropping customerID
    df = df.drop(columns=["customerID"])
    
    # Handling TotalCharges (replacing spaces and converting to float)
    df["TotalCharges"] = df["TotalCharges"].replace({" ": "0.0"})
    df["TotalCharges"] = df["TotalCharges"].astype(float)
    
    # Target distribution
    print("Churn Distribution:")
    print(df["Churn"].value_counts())
    
    print("\n--- Step 3: Preprocessing (Label Encoding) ---")
    object_columns = df.select_dtypes(include="object").columns
    encoders = {}
    for column in object_columns:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        encoders[column] = le
    
    # Save encoders
    with open("encoders.pkl", "wb") as f:
        pickle.dump(encoders, f)
    print("Categorical features encoded and encoders saved.")

    print("\n--- Step 4: Splitting Data and SMOTE ---")
    X = df.drop(columns=["Churn"])
    y = df["Churn"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    smote = SMOTE(random_state=42)
    X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)
    
    print(f"Training set size after SMOTE: {X_train_smote.shape}")
    print(f"Balanced Class Distribution:\n{y_train_smote.value_counts()}")

    print("\n--- Step 5: Model Training (Random Forest) ---")
    # Using Random Forest as it was the best performing model in the notebook
    rfc = RandomForestClassifier(random_state=42)
    rfc.fit(X_train_smote, y_train_smote)
    
    print("\n--- Step 6: Evaluation ---")
    y_pred = rfc.predict(X_test)
    
    print(f"Accuracy Score: {accuracy_score(y_test, y_pred):.4f}")
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Save the model
    with open("churn_model.pkl", "wb") as f:
        pickle.dump(rfc, f)
    print("Model saved as churn_model.pkl")

if __name__ == "__main__":
    run_analysis()
