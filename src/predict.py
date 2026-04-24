import joblib 
from pathlib import Path
import pandas as pd
from typing import TypedDict, List

#metadata for input
class Nutritiondata(TypedDict):
    calories: List[int]
    fat: List[float]
    saturated_fat: List[float]
    carbohydrates: List[float]
    sugars: List[float]
    fiber: List[float]
    proteins: List[float]
    salt: List[float]


# load models 
def load_models(model_name: str = 'gb_pipeline'):
    try:
        models_path = Path(__file__).resolve().parent.parent / 'models' #food_api_project_uv\model
        full_file_path = models_path / f'{model_name}.pkl'
        model = joblib.load(full_file_path)
        return model
    except FileNotFoundError as e:
        
        print(f'{full_file_path} does not exist') 
        raise 
        


# structure mock data 
def mock_datastructure(x: Nutritiondata) -> pd.DataFrame:  
    test_row = pd.DataFrame(x)
    return test_row


# Execute the prediction 
def predict_model (test_row: pd.DataFrame,model: object):
    prediction = model.predict(test_row)
    prediction_prod = model.predict_proba(test_row)[:,1]

    # #simple dict
    output_converter = {0: "Not Healthy", 1: "Healthy"}

    #get the output from prediction
    pred_output = prediction[0]

    #map pred_output to dict 
    output = output_converter.get(pred_output,'unknown')

    final_output = {f'the prediciton is {output} with {prediction_prod} confidence'}


    return final_output
  

        

if __name__ == '__main__':    # check if the code being run is on the same file 

    mock_dict: Nutritiondata = {
            'calories': [150],                    
            'fat': [6.0],                         
            'saturated_fat': [0.5],               
            'carbohydrates': [20.0],              
            'sugars': [8.0],                      
            'fiber': [3.0],                       
            'proteins': [4.0],                    
            'salt': [0.1]                         
    }

    model = load_models()

    test_data =  mock_datastructure(mock_dict)

    result = predict_model(test_data,model)

    print(result)