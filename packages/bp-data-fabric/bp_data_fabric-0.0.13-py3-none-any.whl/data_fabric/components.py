from typing import List
import query_tool as qt
import data_grid as dg
import data_visualization as dv
import streamlit as st

def main(
        query: str = "",
        query_tool_title: str = "",
        data_grid_title: str = "",
        data_visualization_title: str = "",
        databases: List[str] = [],
        tables: List[dict] = [],
        columns: List[dict] = [],
        data={},
        on_database_change=None,
        on_table_change=None,
        on_generate_query=None,
        on_copy_query=None,
        on_execute=None,
        show_data_grid=True,
        show_charts=True,
    ):
    

    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    render_query_tool(
        query=query,
        title=query_tool_title,
        databases=databases,
        tables=tables,
        columns=columns,
        on_database_change=on_database_change,
        on_table_change=on_table_change,
        on_generate_query=on_generate_query,
        on_copy_query=on_copy_query,
    )

    if query != "":
      st.button("Execute", on_click=on_execute)
    st.write("")
    st.write("")
    if show_data_grid == True:
        render_data_grid(
            title=data_grid_title,
            rows=data.get("rows", []),
            columns=data.get("columns", []),
        )

    if show_charts == True:
        render_data_visualizer(
            title=data_visualization_title,
            rows=data.get("rows", []),
        )

def render_query_tool(
        query: str = "",
        title: str = "",
        databases: List[str] = [],
        tables: List[dict] = [],
        columns: List[dict] = [],
        on_database_change=None,
        on_table_change=None,
        on_generate_query=None,
        on_copy_query=None,
):
    qt.query_tool(
        query=query,
        title=title,
        databases=databases,
        tables=tables,
        columns=columns,
        on_database_change=on_database_change,
        on_table_change=on_table_change,
        on_generate_query=on_generate_query,
        on_copy_query=on_copy_query,
        key="query_builder",
    )  

def render_data_grid(title: str="", rows: List = [], columns: List = []):
    dg.data_grid(
        title=title,
        rows=rows,
        columns=columns,
        key="data_grid",
    )

def render_data_visualizer(title="", rows=[]):
    dv.data_visualizer(
        title=title,
        data=rows,
        key="data_visualizer",
    )