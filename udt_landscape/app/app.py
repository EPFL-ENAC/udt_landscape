import streamlit as st
import plotly.express as px
import pandas as pd
from data_wrangling import get_quetions_name,get_themes,get_answers,get_actors



st.set_page_config(layout="wide")

# Sidebar 
df_theme = get_themes()
df_question = get_quetions_name()
df_answer = get_answers()
df_get_actors = get_actors()

df_answer = df_answer.merge(df_get_actors, on='actor id', how='left')
df_answer = df_answer.merge(df_question, on='question id', how='left')
df_answer = df_answer.merge(df_theme, on='theme id', how='left')



with st.sidebar:
    selected_theme = st.selectbox('Select a Theme :', df_theme['theme name'])
    filtered_questions = df_question[df_question['theme id'] == df_theme.loc[df_theme['theme name'] == selected_theme, 'theme id'].values[0]]
    selected_question = st.sidebar.selectbox('Select a Question:', filtered_questions['question name'])

    # add a line 
    st.sidebar.markdown('---')

    # multi select with distinct df_get_actors['actors type']
    selected_actors_type = st.sidebar.multiselect('Select Actors Type:', df_get_actors['actor type'].unique(),default=df_get_actors['actor type'].unique())
    filtered_actor_name = df_get_actors[df_get_actors['actor type'].isin(selected_actors_type)]
    selected_actor_name = st.sidebar.multiselect('Select Actors Name:', filtered_actor_name['actor institution'].unique(),default=filtered_actor_name['actor institution'].unique())



# filter by selected_theme
df_answer = df_answer[df_answer['theme id'] == df_theme.loc[df_theme['theme name'] == selected_theme, 'theme id'].values[0]]
# filter by selected_question
df_answer = df_answer[df_answer['question id'] == filtered_questions.loc[filtered_questions['question name'] == selected_question, 'question id'].values[0]]
# filter by selected_actors_type
df_answer = df_answer[df_answer['actor type'].isin(selected_actors_type)]
# filter by selected_actor_name
df_answer = df_answer[df_answer['actor institution'].isin(selected_actor_name)]



with st.container():
   tab1, tab2, = st.tabs(["Question motivation", "Theme motivation"])
   with tab1:
       st.header("Question motivation")
       st.write(df_answer['question motivation'].values[0])
   with tab2:
       st.header("Theme motivation")
       st.write(df_answer['theme motivation'].values[0])
       
with st.container():
    st.markdown('---')
    # create a piechart based on result colum
    st.header("Analysis")
    st.write(df_answer['question analysis'].values[0])


with st.container():
    st.markdown('---')
    # create a piechart based on result colum
    st.header("Result")
    value_counts = df_answer['result'].value_counts()


    # Create a pie plot using Plotly Express
    fig = px.pie(
        names=value_counts.index,
        values=value_counts.values,
    )

    # Display the pie plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)



with st.container():
    st.markdown('---')
    # create a piechart based on result colum
    st.header("Comments")

    df_comment = df_answer[['actor institution','comment value']].dropna()
    st.write(df_comment)


    # if not pd.isna(df_answer['comment description'].values[0]) : 
    #     st.write(f"{df_answer['comment description'].values[0]} :")
    # else :
    #     st.write("Comment :")

    # st.write(df_answer[['actor institution','comment value']])





st.write(df_answer)





