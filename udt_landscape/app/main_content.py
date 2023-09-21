import json

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
    if not all(df_answer['result'] == "[]") :
        with st.container():
            st.subheader("Results")

            def is_valid_json(json_str):
                try:
                    json.loads(json_str)
                    return True
                except:
                    return False

            def is_list(json_str):
                try:
                    json.loads(json_str)
                    if isinstance(json.loads(json_str), list):
                        return True
                    else:
                        return False
                except:
                    return False

            is_json = df_answer["result"].apply(is_valid_json).all()

            if is_json:
                is_list = df_answer["result"].apply(is_list).all()
                tab1, tab2 = st.tabs(["Plots", "Raw data"])

                if is_list:
                    df_answer["result"] = df_answer["result"].apply(json.loads)
                    df_plot = df_answer.explode("result")[["result"]]
                    with tab1:
                        for col in df_plot.columns:
                            st.write(col)
                            value_counts = df_plot[col].value_counts()
                            fig = px.pie(
                                names=value_counts.index,
                                values=value_counts.values,
                            )
                            st.plotly_chart(fig, use_container_width=True)

                    with tab2:
                        df_raw = df_answer.explode("result")[["actor institution", "result"]]

                        # df_raw_1 = df_answer["actor institution"].reset_index()
                        # df_raw = pd.concat([df_raw_1, df_plot], axis=1)
                        # df_raw = df_raw.drop(columns=["index"])
                        df_raw.rename(columns={"actor institution": "Actor"}, inplace=True)

                        st.dataframe(df_raw, use_container_width=True, hide_index=True)

                else:
                    df_plot = pd.json_normalize(df_answer["result"].apply(json.loads))

                    if question_id in [63, 64]:
                        print(df_plot.columns)

                        with tab1:
                            # bar chart
                            column_sums = df_plot.sum()
                            column_sums_sorted = column_sums.sort_values(ascending=False).to_dict()
                            df = pd.DataFrame(list(column_sums_sorted.items()), columns=["Item", "Occurrence"])
                            st.dataframe(df, use_container_width=True, hide_index=True)

                        with tab2:
                            df_raw_1 = df_answer["actor institution"].reset_index()
                            df_raw = pd.concat([df_raw_1, df_plot], axis=1)
                            df_raw = df_raw.drop(columns=["index"])
                            df_raw.rename(columns={"actor institution": "Actor"}, inplace=True)
                            st.dataframe(df_raw, use_container_width=True, hide_index=True)

                    else:
                        with tab1:
                            for col in df_plot.columns:
                                st.write(col)
                                value_counts = df_plot[col].value_counts()
                                fig = px.pie(
                                    names=value_counts.index,
                                    values=value_counts.values,
                                )
                                st.plotly_chart(fig, use_container_width=True)

                        with tab2:
                            df_raw_1 = df_answer["actor institution"].reset_index()
                            df_raw = pd.concat([df_raw_1, df_plot], axis=1)
                            df_raw = df_raw.drop(columns=["index"])
                            df_raw.rename(columns={"actor institution": "Actor"}, inplace=True)

                            st.dataframe(df_raw, use_container_width=True, hide_index=True)

            else:
                tab1, tab2 = st.tabs(["Plots", "Raw data"])

                with tab1:
                    value_counts = df_answer["result"].value_counts()
                    if value_counts.shape[0] != 0:
                        # Create a pie plot using Plotly Express
                        fig = px.pie(
                            names=value_counts.index,
                            values=value_counts.values,
                        )
                        # Display the pie plot in Streamlit
                        st.plotly_chart(fig, use_container_width=True)

                with tab2:
                    df_raw = df_answer[["actor institution", "result"]]
                    df_raw.rename(columns={"actor institution": "Actor"}, inplace=True)
                    st.dataframe(df_raw, use_container_width=True, hide_index=True)

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
