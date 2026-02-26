import pandas as pd
from pathlib import Path
from typing import Union




def eda_cleaning(input : Union[str, Path], output: Union[str, Path]) -> str:
    df = pd.read_parquet(input)
    df.head()

    #identify duplicate 
    #duplicated = df[df.duplicated()]
    # print(duplicated)

    # -- remove duplicates ---
    df = df.drop_duplicates()

    #check dtypes
    # df.dtypes


    df= df.dropna(subset='nutrition_grade')

    drop_list = ['unknown', 'not applicable']

    # The ~ means "is NOT in"
    df = df[~df['nutrition_grade'].isin(drop_list)]

    #fill nulls with means
    # df = df.fillna(df.mean(numeric_only= True))

    #sugars > carb 
    df = df.query('sugars <= carbohydrates')

    df['healthy_ind'] = df['nutrition_grade'].apply(
        lambda x: 1 if x in ['a','b'] else 0
    )

    df.to_parquet(output)
    return f"saving to {output}"



basepath = Path(__file__).resolve().parent.parent 

output_path = basepath/ 'data' / 'final_data.parquet'
input_path = basepath/ 'data' / 'cleaned_data.parquet'
print('it works at the end')

eda_cleaning(input = input_path, output = output_path)










