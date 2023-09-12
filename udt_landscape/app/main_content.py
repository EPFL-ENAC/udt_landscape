import pandas as pd
import plotly.express as px
import streamlit as st


def main_content(df_answer: pd.DataFrame, question_id: str):
    df_answer = df_answer[df_answer["question id"] == question_id]

    # Add question
    with st.container():
        st.header(df_answer["question name"].values[0])

    # Add question motivation
    with st.container():
        st.subheader("Question motivation")
        st.write(df_answer["question motivation"].values[0])

    # Add analysis
    with st.container():
        # create a piechart based on result colum
        st.subheader("Analysis")
        st.write(df_answer["question analysis"].values[0])

    # Add result
    with st.container():
        value_counts = df_answer["result"].value_counts()
        if value_counts.shape[0] != 0:
            st.subheader("Result")
            # Create a pie plot using Plotly Express
            fig = px.pie(
                names=value_counts.index,
                values=value_counts.values,
            )
            # Display the pie plot in Streamlit
            st.plotly_chart(fig, use_container_width=True)

    # Add remarks
    with st.container():
        matching_columns = [col for col in df_answer.columns if col.startswith("comment description")]

        for i, col in enumerate(matching_columns):
            col_value_name = f"comment value {i}"
            df_filtered = df_answer.dropna(subset=[col_value_name])

            # Add remarks table
            if df_filtered.shape[0]:
                if i == 0:
                    st.subheader("Comments ")
                # Add remarks question
                if not pd.isna(df_answer[col].values[0]):
                    st.write(f"{df_answer[col].values[0]} :")
                else:
                    st.write("Comment :")
                df_filtered2 = df_filtered[["actor institution", col_value_name]]

                # st.table(df_filtered2)
                df_filtered2.rename(columns={"actor institution": "Actor", col_value_name: "Comment"}, inplace=True)

                st.dataframe(df_filtered2, use_container_width=True, hide_index=True)

    st.markdown("---")
