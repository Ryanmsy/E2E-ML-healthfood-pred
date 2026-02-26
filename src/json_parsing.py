import json 
from pathlib import Path 
import sys
import pandas as pd
from typing import Union






def json_parsing(input_path : Union[str,Path], output_path: Union[str,Path])-> pd.DataFrame:
    sys.stdout.reconfigure(encoding='utf-8')


    try:
        with open(input_path, 'r', encoding='utf-8', errors="replace") as f: 
            data = json.load(f)
            #print(len(data))
            # Change this line:
            #print(json.dumps(data[:14], indent= 4))
            
            # Or use repr(), which is similar:
            # print(f"{repr(data)} and {len(data)}")

    except Exception as e:
        data = []
        print(e)
        return None

    def parse_product(product):
        # Extract the nested 'nutriments' dictionary
        nutrients = product.get('nutriments', {})
        
        return {
            'product_name': product.get('product_name', 'Unknown'),
            'nutrition_grade': product.get('nutrition_grades', None),
            
            # Extract specific nutrients (default to None if missing)
            # Note: OFF uses keys like 'sugars_100g' for values per 100g/ml
            'calories': nutrients.get('energy-kcal_100g'),
            'fat': nutrients.get('fat_100g'),
            'saturated_fat': nutrients.get('saturated-fat_100g'),
            'carbohydrates': nutrients.get('carbohydrates_100g'),
            'sugars': nutrients.get('sugars_100g'),
            'fiber': nutrients.get('fiber_100g'),
            'proteins': nutrients.get('proteins_100g'),
            'salt': nutrients.get('salt_100g')
        }

    # 3. Apply the function to the list of dictionaries
    parsed_data = [parse_product(p) for p in data]


    # 4. Create the DataFrame
    df = pd.DataFrame(parsed_data)
    df.to_parquet(output_path)
    print(f"Saved to {output_path}")
    return df

base_path = Path(__file__).resolve().parent.parent

raw_file = base_path / 'data' / 'raw_product_data.json'

processed_file = base_path / 'data' / 'cleaned_data.parquet'


json_parsing(input_path = raw_file, output_path = processed_file)