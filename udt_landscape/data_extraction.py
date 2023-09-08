import os
import pandas as pd
from itertools import takewhile

current_path_path = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.dirname(current_path_path)
DATA_PATH = os.path.join(root_folder, "data","Urban Digital Twin SGS Office.xlsx")
SHEET_NAME = "Urban Digital Twin SGS Office"



def load_data() -> pd.DataFrame:
    df = pd.read_excel(DATA_PATH, sheet_name=SHEET_NAME,engine='openpyxl')
    return df


def data_cleasing(df : pd.DataFrame) -> pd.DataFrame:
    # remove row without email
    df = df[df['E-mail'].notna()]
    return df


def get_specific_question(df : pd.DataFrame, question_id : str) -> pd.DataFrame:

    # list of columns in the dataframe
    columns = df.columns.tolist()
    question_column_name = [str(item) for item in columns if str(item).startswith(f"{question_id} - ")][0]
    index = columns.index(question_column_name)
    answer_columns = list(takewhile(lambda element: not str(element).startswith("Unnamed"), columns[index + 1:]))
    selected_columns = ['E-mail']+[question_column_name] + answer_columns
    df = df[selected_columns]
    df = data_cleasing(df)


    def get_column_name(row):
        columns_with_ones = row.index[row == 1]
        if len(columns_with_ones) > 0:
            return columns_with_ones[0]
        else:
            return None
        
    df['result'] = df.apply(get_column_name, axis=1)
    df['result'] = df['result'].str.replace(r'\.\d+$', '', regex=True)



    desired_order = ['E-mail', 'result'] + answer_columns

    df = df[desired_order]


    return df

def save_to_excel(df : pd.DataFrame, file_name : str):
    df.to_excel(file_name, index=False)



if __name__ == "__main__":

    q = 6
    df = load_data()
    df = get_specific_question(df, q)
    # print(df.head())
    save_to_excel(df, os.path.join(root_folder, "data",f"temp{q}.xlsx"))
