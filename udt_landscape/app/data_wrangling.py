import pandas as pd

SHEET_ID = "1nkN9_fpi-DsQwxTzQA2wJPBlBB5Pd3UN1EXPuQBEKzk"


def get_data(sheet_name: str) -> pd.DataFrame:
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    df = pd.read_csv(url)
    return df


def get_quetions_name() -> pd.DataFrame:
    df = get_data("questions")
    # df = df[['question id','question name','theme id']]

    return df


def get_themes() -> pd.DataFrame:
    df = get_data("themes")
    return df


def get_answers() -> pd.DataFrame:
    df = get_data("answers")
    return df


def get_actors() -> pd.DataFrame:
    df = get_data("actors")
    return df


if __name__ == "__main__":
    print(get_quetions_name())
