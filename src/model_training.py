import pandas as pd 
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import joblib


def data_loading():
    basepath = Path(__file__).resolve().parent.parent

    input_path = basepath / 'data' / 'final_data.parquet'
    
    df = pd.read_parquet(input_path)
    print(basepath)
    return df


def data_preprocess(df : pd.DataFrame):
    #  --- X and Y init --- 
    X = df.drop(columns= ['healthy_ind']).select_dtypes(exclude = ['object'])
    y = df['healthy_ind'] 

    #Target variable imbalance - stratifed splitting(ensure even number of variables) 
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size= 0.2,
        random_state= 12345,
        stratify= y 
    )
    #print(f"data_prep: {locals()}")
    return X_train, X_test, y_train, y_test, X,y

    #--- fill nulls to prevent data leakage --- 
    # train_means = X_train.mean(numeric_only = 'True')

    # X_train = X_train.fillna(train_means)
    # X_test = X_test.fillna(train_means)

def impute(X_train, X_test ):
    imputer = SimpleImputer(
        missing_values = np.nan,
        strategy = 'mean'
    )

    X_train = imputer.fit_transform(X_train)
    X_test = imputer.transform(X_test)
    return X_train, X_test, imputer
    #do we transform now?

#encodings (none because no cateogorical data)

#feature scaling (normalization)
    #min max
    #z score 
    # l2 norm for distance like text

def scaling(X_train, X_test):
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    return X_train, X_test, scaler


def random_forest(X_train, y_train):
    regressor = RandomForestClassifier(random_state= 12345)
    regressor.fit(X_train, y_train)
    return regressor


def model_int(X_train, y_train):
    #model training
    model = LogisticRegression()
    model.fit(X_train, y_train)
    return model 



def evaluate_model(X_train, X_test, y_train, y_test, X, model): 
    # train accuracy
    y_train_pred = model.predict(X_train)
    train_accuracy = accuracy_score(y_train, y_train_pred)

    # test accuracy
    y_test_pred = model.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_test_pred)

    # Confusion Matrix
    matrix = confusion_matrix(y_test, y_test_pred)
    print("Confusion Matrix:")
    print(matrix, "\n")

    # Classification Report (Detailed breakdown)
    report = classification_report(y_test, y_test_pred)
    print("Classification Report:")
    print(report)

    # --- Feature Importances / Coefficients --- 
    feature_names = X.columns

    # Use a single variable name (importance_vals) for all branches
    if hasattr(model, 'coef_'):
        importance_vals = model.coef_[0]
    elif hasattr(model, 'feature_importances_'):
        importance_vals = model.feature_importances_
    else: 
        importance_vals = np.zeros(len(feature_names))

    # Create the dataframe using the unified variable
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importance_vals
    })

    # Optional: Sort the dataframe to see the most important features at the top
    importance_df = importance_df.sort_values(by='Importance', ascending=False)
    
    print("Feature Importances:")
    print(importance_df)
    print("\n" + "="*40 + "\n")
    #next step is random forest tree 

    # or hyper parameters

if __name__ == "__main__":

    #1  load
    df = data_loading()

# 2. Split
    X_train, X_test, y_train, y_test, X,y = data_preprocess(df)

    #3 Impute 
    X_train, X_test, imputer = impute(X_train, X_test)

    #4. scaling
    X_train, X_test, scaler = scaling(X_train, X_test)

    print("========== LOGISTIC REGRESSION ==========")
    log_model = model_int(X_train, y_train)
    evaluate_model(X_train, X_test, y_train, y_test, X, log_model)

# --- Run Random Forest ---
    print("========== RANDOM FOREST ==========")
    print("testing git add")
    rf_model = random_forest(X_train, y_train)
    evaluate_model(X_train, X_test, y_train, y_test, X, rf_model)

    # --- Save models and preprocessing artifacts ---
    models_path = Path(__file__).resolve().parent.parent / 'models'
    models_path.mkdir(exist_ok=True)

    joblib.dump(imputer, models_path / 'imputer.pkl')
    joblib.dump(scaler,  models_path / 'scaler.pkl')
    joblib.dump(log_model, models_path / 'logistic_regression.pkl')
    joblib.dump(rf_model, models_path / 'random_forest.pkl')
    print(f"Models saved to {models_path}")
