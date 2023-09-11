import numpy as np
import pandas as pd
import streamlit as st
from data_wrangling import get_actors, get_answers, get_quetions_name, get_themes
from main_content import main_content

st.set_page_config(layout="wide")

# Sidebar
df_theme = get_themes()
df_question = get_quetions_name()
df_answer = get_answers()
df_get_actors = get_actors()

df_answer = df_answer.merge(df_get_actors, on="actor id", how="left")
df_answer = df_answer.merge(df_question, on="question id", how="left")
df_answer = df_answer.merge(df_theme, on="theme id", how="left")


with st.sidebar:
    selected_theme = st.selectbox("Select a Theme :", df_theme["theme name"])
    filtered_questions = df_question[
        df_question["theme id"] == df_theme.loc[df_theme["theme name"] == selected_theme, "theme id"].values[0]
    ]
    filtered_questions = filtered_questions[filtered_questions["question alias"].notna()]
    # add a top row to df_question
    new_row = {"question id": "all", "question alias": "All"}
    for col in filtered_questions.columns[2:]:
        new_row[col] = np.nan
    filtered_questions = pd.concat([pd.DataFrame(new_row, index=[0]), filtered_questions]).reset_index(drop=True)

    selected_question = st.sidebar.selectbox("Select a Question:", filtered_questions["question alias"])

    # add a line
    st.sidebar.markdown("---")

    # multi select with distinct df_get_actors['actors type']
    selected_actors_type = st.sidebar.multiselect(
        "Select Actors Type:", df_get_actors["actor type"].unique(), default=df_get_actors["actor type"].unique()
    )
    filtered_actor_name = df_get_actors[df_get_actors["actor type"].isin(selected_actors_type)]
    selected_actor_name = st.sidebar.multiselect(
        "Select Actors Name:",
        filtered_actor_name["actor institution"].unique(),
        default=filtered_actor_name["actor institution"].unique(),
    )


# filter by selected_theme
df_answer = df_answer[
    df_answer["theme id"] == df_theme.loc[df_theme["theme name"] == selected_theme, "theme id"].values[0]
]
# filter by selected_question
# filter by selected_actors_type
df_answer = df_answer[df_answer["actor type"].isin(selected_actors_type)]
# filter by selected_actor_name
df_answer = df_answer[df_answer["actor institution"].isin(selected_actor_name)]


with st.container():
    st.header("Theme motivation")
    st.write(df_answer["theme motivation"].values[0])


# Get the question id
question_id = filtered_questions.loc[filtered_questions["question alias"] == selected_question, "question id"].values[0]
question_id_list = []


if question_id == "all":
    # get all question_id in df_answer
    question_id_list = list(df_answer["question id"].unique())
    question_id_list = [int(x) for x in question_id_list]
else:
    question_id_list = [question_id]
    if df_answer[df_answer["question id"] == question_id]["follow up question id"].notna().any():
        follow_up_question_id = df_answer[df_answer["question id"] == question_id]["follow up question id"].values[0]
        follow_up_question_id_list = follow_up_question_id.split(",")
        follow_up_question_id_list = [int(x) for x in follow_up_question_id_list]
        question_id_list += follow_up_question_id_list


# Add main content
for question_id in question_id_list:
    main_content(df_answer, question_id)
