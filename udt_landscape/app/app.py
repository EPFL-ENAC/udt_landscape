import os
import sys
import numpy as np
import pandas as pd
import streamlit as st
from data_wrangling import get_actors, get_answers, get_quetions_name, get_themes
from main_content import main_content
from PIL import Image
from images_markdown import markdown_insert_images

st.set_page_config(layout="wide")

try :
    # Add a title
    mode = sys.argv[1]
    if mode in ['private','Private']:
        is_private = True
    else:
        is_private = False
except:
    is_private = False


# Sidebar
df_theme = get_themes()

# Add a new row to the df_theme DataFrame
intro_conlusion = ["Survey Introduction","Survey conclusion"]
folder_name_intro_conlusion = ["introduction_md","conclusion_md"]
new_row = {"theme id": 0, "theme name": intro_conlusion[0]}
df_theme = pd.concat([pd.DataFrame(new_row, index=[0]), df_theme]).reset_index(drop=True)
new_row = {"theme id": 7, "theme name": intro_conlusion[1]}
df_theme = pd.concat([df_theme,pd.DataFrame(new_row, index=[7])]).reset_index(drop=True)



df_question = get_quetions_name()
df_answer = get_answers()
df_get_actors = get_actors()

df_answer = df_answer.merge(df_get_actors, on="actor id", how="left")
df_answer = df_answer.merge(df_question, on="question id", how="left")
df_answer = df_answer.merge(df_theme, on="theme id", how="left")






with st.sidebar:

    # add image
    file_path = os.path.join(os.path.dirname(__file__), "static", "Logo-SGS-MSWord-Header-transparent.png")
    if os.path.exists(file_path):
        image = Image.open(file_path)
        # st.image(image, width= use_column_width=True)
        st.sidebar.image(image)

        
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

    if is_private :
        filtered_actor_name = df_get_actors[df_get_actors["actor type"].isin(selected_actors_type)]
        selected_actor_name = st.sidebar.multiselect(
            "Select Actors Name:",
            filtered_actor_name["actor institution"].unique(),
            default=filtered_actor_name["actor institution"].unique(),
        )

    
    if is_private :
        st.write("This is the private version of the tool.")
    else:
        st.write("This is the public version of the tool. Data has been anonymized.")


if selected_theme in  intro_conlusion :
    index = intro_conlusion.index(selected_theme)
    folder_name = folder_name_intro_conlusion[index]
    folder = os.path.join(os.path.dirname(__file__), "static",folder_name)
    # Find the first file with the ".md" extension in the folder
    file_path = next((os.path.join(folder, file_name) for file_name in os.listdir(folder) if file_name.endswith(".md")), None)

    # If no file with the ".md" extension is found, raise an error
    if not file_path:
        raise FileNotFoundError("No markdown file found in the folder.")
    
    with open(file_path, "r") as readme_file:
        readme = readme_file.read()
    readme = markdown_insert_images(readme,folder_name)
    st.markdown(readme, unsafe_allow_html=True)



else : 


    # filter by selected_theme
    df_answer = df_answer[
        df_answer["theme id"] == df_theme.loc[df_theme["theme name"] == selected_theme, "theme id"].values[0]
    ]
    # filter by selected_question
    # filter by selected_actors_type
    df_answer = df_answer[df_answer["actor type"].isin(selected_actors_type)]
    # filter by selected_actor_name
    if is_private :
        df_answer = df_answer[df_answer["actor institution"].isin(selected_actor_name)]





    # Get the question id
    question_id = filtered_questions.loc[filtered_questions["question alias"] == selected_question, "question id"].values[0]
    question_id_list = []

    with st.container():
        if question_id == "all":
            st.header("Theme")
            tab1, tab2 = st.tabs(["Theme motivation", "Theme analysis"])
            with tab1:
                st.write(df_answer["theme motivation"].values[0])
            with tab2:
                st.write(df_answer["theme analysis"].values[0])

    if question_id == "all":
        # get all question_id in df_answer
        question_id_list = list(df_answer["question id"].unique())
        question_id_list = [int(x) for x in question_id_list]
    else:
        question_id_list = [question_id]
        if df_answer[df_answer["question id"] == question_id]["follow up question id"].notna().any():
            follow_up_question_id = df_answer[df_answer["question id"] == question_id]["follow up question id"].values[0]
            if "," in str(follow_up_question_id):
                follow_up_question_id_list = follow_up_question_id.split(",")
                follow_up_question_id_list = [int(x) for x in follow_up_question_id_list if x]
            else:
                follow_up_question_id_list = [int(follow_up_question_id)]

            question_id_list += follow_up_question_id_list


    if not is_private :
        df_answer['actor name'] = df_answer['actor anonymous']
        df_answer['actor institution'] = df_answer['actor anonymous']




    # Add main content
    for question_id in question_id_list:
        main_content(df_answer, question_id)
