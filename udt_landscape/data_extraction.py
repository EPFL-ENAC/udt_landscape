import os
from itertools import takewhile

import pandas as pd

current_path_path = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.dirname(current_path_path)
DATA_PATH = os.path.join(root_folder, "data", "Urban Digital Twin SGS Office.xlsx")
SHEET_NAME = "Urban Digital Twin SGS Office"


def load_data() -> pd.DataFrame:
    df = pd.read_excel(DATA_PATH, sheet_name=SHEET_NAME, engine="openpyxl")
    return df


def data_cleasing(df: pd.DataFrame) -> pd.DataFrame:
    # remove row without email
    df = df[df["E-mail"].notna()]
    return df


def get_specific_question(df: pd.DataFrame, question_id: int) -> pd.DataFrame:
    # list of columns in the dataframe

    df_result = pd.DataFrame()

    if question_id == 41:
        pass
    else:
        columns = df.columns.tolist()
        print(question_id)
        list_question_column_name = [str(item) for item in columns if str(item).startswith(f"{question_id} - ")]
        if list_question_column_name:
            question_column_name = list_question_column_name[0]
            index = columns.index(question_column_name)

            # answer
            answer_columns = list(
                takewhile(lambda element: not str(element).startswith("Unnamed"), columns[index + 1 :])
            )
            df_answer = df[answer_columns]
            answer_columns_without_remark = df_answer.columns[(df_answer.eq(1) | df_answer.isnull()).all()].tolist()
            df_answer_without_remark = df[answer_columns_without_remark]
            answer_column_remark = [item for item in answer_columns if item not in answer_columns_without_remark]
            df_remark = df[answer_column_remark]

            def get_column_name(row):
                columns_with_ones = row.index[row == 1]
                if len(columns_with_ones) > 0:
                    return columns_with_ones[0]
                else:
                    return None

            df_answer_without_remark["result"] = df_answer_without_remark.apply(get_column_name, axis=1)
            try:
                df_answer_without_remark["result"] = df_answer_without_remark["result"].str.replace(
                    r"\.\d+$", "", regex=True
                )
            except:
                pass
            df_answer_without_remark = df_answer_without_remark["result"]

            df_result = df[["E-mail"]]
            df_result = pd.concat([df_result, df_answer_without_remark], axis=1)
            df_result = data_cleasing(df_result)
            df_result.insert(0, "question id", question_id)

            for i, item in enumerate(answer_column_remark):
                print(item)
                col_name = f"comment description {i}"
                df_result[col_name] = item
                col_name = f"comment value {i}"
                df_result[col_name] = df_remark[item]

            # selected_columns = ["E-mail"] + [question_column_name] + answer_columns
            # df = df[selected_columns]
            # print(df.head())

            # desired_order = ["E-mail", "result"] + answer_columns

            # df = df[desired_order]

    return df_result


def save_to_excel(df: pd.DataFrame, file_name: str):
    df.to_excel(file_name, index=False)


def process():
    df = load_data()

    df_result = pd.DataFrame()
    for i in range(1, 65):
        df_one_question = get_specific_question(df, i)
        # append to df_result
        df_result = pd.concat([df_result, df_one_question], ignore_index=True)

    save_to_excel(df_result, os.path.join(root_folder, "data", "temp.xlsx"))


if __name__ == "__main__":
    process()
    # for i in range(1,65) :
    #     df = load_data()
    #     df = get_specific_question(df, i)
    #     # print(df.head())
    #     save_to_excel(df, os.path.join(root_folder, "data", f"temp{i}.xlsx"))
    # i = 11
    # df = load_data()
    # df = get_specific_question(df, i)
    # save_to_excel(df, os.path.join(root_folder, "data", f"temp{i}.xlsx"))
