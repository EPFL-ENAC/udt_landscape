import json
import os
from itertools import takewhile
import re

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
    columns = df.columns.tolist()

    def get_column_name(row):
        columns_with_ones = row.index[row == 1]
        if len(columns_with_ones) > 0:
            return columns_with_ones[0]
        else:
            return None

    list_question_column_name = [str(item) for item in columns if str(item).startswith(f"{question_id} - ")]
    if list_question_column_name:
        question_column_name = list_question_column_name[0]
        index = columns.index(question_column_name)

        # answer
        answer_columns = list(takewhile(lambda element: not str(element).startswith("Unnamed"), columns[index + 1 :]))
        df_answer = df[answer_columns]

        if question_id == 41:
            question_column_name = [str(item) for item in columns if str(item).startswith(f"{question_id} - ")][0]
            index = columns.index(question_column_name)
            start_index = index + 2
            end_index = index + 102

            list_columns_name = columns[start_index:end_index]
            df_answer_without_remark_1 = df[list_columns_name]

            df_answer_without_remark_1["result"] = df_answer_without_remark_1.apply(get_column_name, axis=1)
            df_answer_without_remark = df_answer_without_remark_1["result"]

            def uniform_value(cell_value):
                if cell_value > 0 and cell_value < 10:
                    return "0 - 10 %"
                elif cell_value >= 10 and cell_value < 25:
                    return "10 - 25 %"
                elif cell_value >= 25 and cell_value < 50:
                    return "25 - 50 %"
                elif cell_value >= 50 and cell_value < 75:
                    return "50 - 75 %"
                elif cell_value >= 75 and cell_value < 100:
                    return "75 - 100 %"
                elif cell_value == 100:
                    return "100 %"

            df_answer_without_remark = df_answer_without_remark.map(uniform_value)

            answer_column_remark = [
                "Do you have the intention to increase this number? Please descibe your motivation, constraints and any"
                " other remarks."
            ]
            df_remark = df[answer_column_remark]

        elif question_id in [61]:
            df_answer_without_remark = pd.DataFrame()
            df_answer_json = pd.DataFrame()
            list_header = []
            list_header.append(
                [
                    "No (1)",
                    "No, but we are investigating this (2)",
                    "Yes (3)",
                    "I don't know (4)",
                ]
            )

            for i in range(1, 7):
                list_header.append(
                    [
                        f"No (1).{i}",
                        f"No, but we are investigating this (2).{i}",
                        f"Yes (3).{i}",
                        f"I don't know (4).{i}",
                    ]
                )
            list_name = []
            list_name.append("Traffic and Transportation")
            list_name.append("Land Use and Zoning")
            list_name.append("Environmental and Sustainability")
            list_name.append("Emergency Response and Disaster Management")
            list_name.append("Social and Demographic")
            list_name.append("Economic and Real Estat")
            list_name.append("Energy and Utility Systems")

            print(df_answer.columns)

            for i in range(len(list_header)):
                header = list_header[i]
                name = list_name[i]

                print(header)
                print(name)

                df_answer_1 = df_answer[header]
                df_answer_1[name] = df_answer_1.apply(get_column_name, axis=1)
                df_answer_1[name] = df_answer_1[name].str.replace(r"\s*\(\s*\d+\s*\)\s*", "", regex=True)
                df_answer_1[name] = df_answer_1[name].str.replace(r"\.\d+$", "", regex=True)
                df_answer_1 = df_answer_1[name]

                df_answer_json = pd.concat([df_answer_json, df_answer_1], axis=1)
                df_answer_without_remark["result"] = df_answer_json.apply(lambda row: json.dumps(row.to_dict()), axis=1)

            answer_column_remark = [
                "Please, provide any details on the type of models used (e.g., AI, empirical models, physically based)"
            ]
            df_remark = df[answer_column_remark]

        elif question_id in [53]:
            df_answer_without_remark = pd.DataFrame()
            df_answer_json = pd.DataFrame()
            list_header = []
            list_header.append(
                [
                    "Yes, we are currently using this. (1)",
                    "No, but we are investigating this. (2)",
                    "No. (3)",
                    "I don't know what it is. (4)",
                ]
            )
            list_header.append(
                [
                    "Yes, we are currently using this. (1).1",
                    "No, but we are investigating this. (2).1",
                    "No. (3).1",
                    "I don't know what it is. (4).1",
                ]
            )
            list_header.append(
                [
                    "Yes, we are currently using this. (1).2",
                    "No, but we are investigating this. (2).2",
                    "No. (3).2",
                    "I don't know what it is. (4).2",
                ]
            )
            list_header.append(
                [
                    "Yes, we are currently using this. (1).3",
                    "No, but we are investigating this. (2).3",
                    "No. (3).3",
                    "I don't know what it is. (4).3",
                ]
            )
            list_header.append(
                [
                    "Yes, we are currently using this. (1).4",
                    "No, but we are investigating this. (2).4",
                    "No. (3).4",
                    "I don't know what it is. (4).4",
                ]
            )
            list_header.append(
                [
                    "Yes, we are currently using this. (1).5",
                    "No, but we are investigating this. (2).5",
                    "No. (3).5",
                    "I don't know what it is. (4).5",
                ]
            )
            list_header.append(
                [
                    "Yes, we are currently using this. (1).6",
                    "No, but we are investigating this. (2).6",
                    "No. (3).6",
                    "I don't know what it is. (4).6",
                ]
            )
            list_name = []
            list_name.append("Apache Sedona")
            list_name.append("Apache Spark")
            list_name.append("Python code (opensource libraries)")
            list_name.append("Python ArcPy")
            list_name.append("FME")
            list_name.append("FME server")
            list_name.append("Apache Kafka")

            for i in range(len(list_header)):
                header = list_header[i]
                name = list_name[i]

                df_answer_1 = df_answer[header]
                df_answer_1[name] = df_answer_1.apply(get_column_name, axis=1)
                df_answer_1[name] = df_answer_1[name].str.replace(r"\s*\(\s*\d+\s*\)\s*", "", regex=True)
                df_answer_1[name] = df_answer_1[name].str.replace(r"\.\d+$", "", regex=True)
                df_answer_1 = df_answer_1[name]

                df_answer_json = pd.concat([df_answer_json, df_answer_1], axis=1)
                df_answer_without_remark["result"] = df_answer_json.apply(lambda row: json.dumps(row.to_dict()), axis=1)

            answer_column_remark = ["An other procesing tool not listed above, please write it down here"]
            df_remark = df[answer_column_remark]

        elif question_id in [63]:
            df_answer_without_remark_1 = df_answer.drop("Something else, please explain…", axis=1)

            df_answer_without_remark_1["result"] = df_answer_without_remark_1.apply(
                lambda row: json.dumps(row.to_dict()), axis=1
            )

            df_answer_without_remark = df_answer_without_remark_1["result"]

            answer_column_remark = ["Something else, please explain…"]
            df_remark = df[answer_column_remark]

        elif question_id in [64]:
            print(df_answer.columns)

            df_answer_without_remark_1 = df_answer.drop("Something else, please explain….1", axis=1)

            df_answer_without_remark_1["result"] = df_answer_without_remark_1.apply(
                lambda row: json.dumps(row.to_dict()), axis=1
            )

            df_answer_without_remark = df_answer_without_remark_1["result"]

            answer_column_remark = ["Something else, please explain….1"]
            df_remark = df[answer_column_remark]

        elif question_id in [32]:
            df_answer_without_remark = pd.DataFrame()
            df_answer_json = pd.DataFrame()
            list_header = []
            list_header.append(
                [
                    "Yes (1)",
                    "No, but planned in a short term (2)",
                    "No, unplanned (3)",
                    "Not considered or unknown (4)",
                ]
            )
            list_header.append(
                [
                    "Yes (1).1",
                    "No, but planned in a short term (2).1",
                    "No, unplanned (3).1",
                    "Not considered or unknown (4).1",
                ]
            )
            list_header.append(
                [
                    "Yes (1).2",
                    "No, but planned in a short term (2).2",
                    "No, unplanned (3).2",
                    "Not considered or unknown (4).2",
                ]
            )
            list_header.append(
                [
                    "Yes (1).3",
                    "No, but planned in a short term (2).3",
                    "No, unplanned (3).3",
                    "Not considered or unknown (4).3",
                ]
            )
            list_header.append(
                [
                    "Yes (1).4",
                    "No, but planned in a short term (2).4",
                    "No, unplanned (3).4",
                    "Not considered or unknown (4).4",
                ]
            )
            list_header.append(
                [
                    "Yes (1).5",
                    "No, but planned in a short term (2).5",
                    "No, unplanned (3).5",
                    "Not considered or unknown (4).5",
                ]
            )

            list_name = []
            list_name.append("Remote sensing (raster) data")
            list_name.append("LIDAR data")
            list_name.append("Human surveyed data")
            list_name.append("Sensors (IoT) data")
            list_name.append("Social media data")
            list_name.append("Citizen reports data")

            for i in range(len(list_header)):
                header = list_header[i]
                name = list_name[i]

                df_answer_1 = df_answer[header]
                df_answer_1[name] = df_answer_1.apply(get_column_name, axis=1)
                df_answer_1[name] = df_answer_1[name].str.replace(r"\s*\(\s*\d+\s*\)\s*", "", regex=True)
                df_answer_1[name] = df_answer_1[name].str.replace(r"\.\d+$", "", regex=True)
                df_answer_1 = df_answer_1[name]

                df_answer_json = pd.concat([df_answer_json, df_answer_1], axis=1)
                df_answer_without_remark["result"] = df_answer_json.apply(lambda row: json.dumps(row.to_dict()), axis=1)

            df_answer_json.to_pickle(
                os.path.join(current_path_path, "app", "32.pkl"),
                compression="infer",
                protocol=5,
                storage_options=None,
            )
            answer_column_remark = [
                'If you selected "yes", please describe briefly the type of data you are using and its purpose:'
            ]
            df_remark = df[answer_column_remark]

        elif question_id in [38]:
            answer_columns_without_remark = df_answer.columns[(df_answer.eq(1) | df_answer.isnull()).all()].tolist()
            df_answer_without_remark = df[answer_columns_without_remark]

            answer_column_remark = [item for item in answer_columns if item not in answer_columns_without_remark]
            df_remark = df[answer_column_remark]
            

            # rename column
            print(df_remark.columns)
            df_remark = df_remark.rename(columns=
                {
                    "Vector datasets ___": "Vector datasets",
                    "Raster datasets ___": "LIDAR datasets",
                    "LIDAR datasets ___": "Raster datasets",

                }
            )

            answer_column_remark = ['Vector datasets', 'Raster datasets', 'LIDAR datasets']

            def get_columns_with_1(row):
                r = [col for col in df_answer_without_remark.columns if row[col] == 1]
                return json.dumps(r)

            df_answer_without_remark["result"] = df_answer_without_remark.apply(get_columns_with_1, axis=1)

            try:
                df_answer_without_remark["result"] = df_answer_without_remark["result"].str.replace(
                    r"\.\d+", "", regex=True
                )
            except:
                pass

            df_answer_without_remark = df_answer_without_remark["result"]

            

            


        
        else:
            answer_columns_without_remark = df_answer.columns[(df_answer.eq(1) | df_answer.isnull()).all()].tolist()
            df_answer_without_remark = df[answer_columns_without_remark]

            answer_column_remark = [item for item in answer_columns if item not in answer_columns_without_remark]
            df_remark = df[answer_column_remark]

            def get_columns_with_1(row):
                r = [col for col in df_answer_without_remark.columns if row[col] == 1]
                return json.dumps(r)

            df_answer_without_remark["result"] = df_answer_without_remark.apply(get_columns_with_1, axis=1)

            try:
                df_answer_without_remark["result"] = df_answer_without_remark["result"].str.replace(
                    r"\.\d+", "", regex=True
                )
            except:
                pass

            df_answer_without_remark = df_answer_without_remark["result"]

        # else:

        # answer_columns_without_remark = df_answer.columns[(df_answer.eq(1) | df_answer.isnull()).all()].tolist()
        # df_answer_without_remark = df[answer_columns_without_remark]
        # answer_column_remark = [item for item in answer_columns if item not in answer_columns_without_remark]
        # df_remark = df[answer_column_remark]

        # df_answer_without_remark["result"] = df_answer_without_remark.apply(get_column_name, axis=1)
        # try:
        #     df_answer_without_remark["result"] = df_answer_without_remark["result"].str.replace(
        #         r"\.\d+$", "", regex=True
        #     )
        # except:
        #     pass
        # df_answer_without_remark = df_answer_without_remark["result"]

        df_result = df[["E-mail"]]
        df_result = pd.concat([df_result, df_answer_without_remark], axis=1)
        df_result = data_cleasing(df_result)
        df_result.insert(0, "question id", question_id)

        for i, item in enumerate(answer_column_remark):
            col_name = f"comment description {i}"
            df_result[col_name] = item
            col_name = f"comment value {i}"
            df_result[col_name] = df_remark[item]

        # selected_columns = ["E-mail"] + [question_column_name] + answer_columns
        # df = df[selected_columns]
        # print(df.head())

        # desired_order = ["E-mail", "result"] + answer_columns

        # df = df[desired_order]

        def empty_if_contains_underscore(cell_value):
            if "___" in str(cell_value):
                return ""
            return cell_value

        def empty_if_comment_dit(cell_value):
            if "Comments." in str(cell_value) or "undefined" in str(cell_value):
                return ""
            return cell_value
        
        def empty_if_comment_2(cell_value):
            if "." in str(cell_value) : 
                return re.sub(r'\.\d+\s*$', '', cell_value)
            return cell_value

        df_result = df_result.map(empty_if_contains_underscore)
        df_result = df_result.map(empty_if_comment_dit)
        df_result = df_result.map(empty_if_comment_2)

    return df_result


def save_to_excel(df: pd.DataFrame, file_name: str):
    # rename one column
    df = df.rename(columns={"E-mail": "actor id"})
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

    # i = 39
    # df = load_data()
    # df = get_specific_question(df, i)
    # save_to_excel(df, os.path.join(root_folder, "data", f"temp{i}.xlsx"))
