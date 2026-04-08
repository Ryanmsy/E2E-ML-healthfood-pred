import pandas as pd
import numpy as np
import joblib
from pathlib import Path


FEATURE_COLUMNS = [
    'calories',
    'fat',
    'saturated_fat',
    'carbohydrates',
    'sugars',
    'fiber',
    'proteins',
    'salt',
]

def load_artifacts(model_name: str = 'random_forest'):
    """
    Load preprocessing artifacts and a trained model from models/.

    Args:
        model_name: 'random_forest' or 'logistic_regression'

    Returns:
        imputer, scaler, model
    """
    models_path = Path(__file__).resolve().parent.parent / 'models'

    imputer = joblib.load(models_path / 'imputer.pkl')
    scaler  = joblib.load(models_path / 'scaler.pkl')
    model   = joblib.load(models_path / f'{model_name}.pkl')

    return imputer, scaler, model


def predict(input_data: dict, model_name: str = 'random_forest') -> dict:
    """
    Predict whether a food product is healthy based on its nutrient values.

    Args:
        input_data: dict with keys matching FEATURE_COLUMNS.
                    Missing nutrients default to NaN and are imputed.
        model_name: which trained model to use ('random_forest' or 'logistic_regression')

    Returns:
        dict with:
            'prediction'  - 1 (healthy) or 0 (not healthy)
            'probability' - confidence score for the predicted class
            'label'       - human-readable label
    """
    imputer, scaler, model = load_artifacts(model_name)

    # Build a single-row DataFrame, filling any missing columns with NaN
    row = {col: input_data.get(col, np.nan) for col in FEATURE_COLUMNS}
    X = pd.DataFrame([row], columns=FEATURE_COLUMNS)

    # Apply the same preprocessing used during training (transform only, not fit)
    X_imputed = imputer.transform(X)
    X_scaled  = scaler.transform(X_imputed)

    prediction = int(model.predict(X_scaled)[0])

    if hasattr(model, 'predict_proba'):
        probability = float(model.predict_proba(X_scaled)[0][prediction])
    else:
        probability = None

    return {
        'prediction':  prediction,
        'probability': probability,
        'label':       'healthy' if prediction == 1 else 'not healthy',
    }


if __name__ == '__main__':
    # Example: a product with known nutrient values
    sample_product = {
        'calories':      52.0,
        'fat':           0.2,
        'saturated_fat': 0.0,
        'carbohydrates': 14.0,
        'sugars':        10.0,
        'fiber':         2.4,
        'proteins':      0.3,
        'salt':          0.0,
    }

    result = predict(sample_product, model_name='random_forest')
    print(f"Prediction : {result['label']} ({result['prediction']})")
    print(f"Confidence : {result['probability']:.2%}" if result['probability'] else "No probability available")
