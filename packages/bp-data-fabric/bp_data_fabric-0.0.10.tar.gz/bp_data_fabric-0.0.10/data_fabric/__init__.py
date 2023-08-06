from typing import List
from data_fabric.components import main

def data_fabric(
    query: str = "",
    query_tool_title: str = "",
    data_grid_title: str = "",
    data_visualization_title: str = "",
    databases: List[str] = [],
    tables: List[dict] = [],
    columns: List[dict] = [],
    on_database_change=None,
    on_table_change=None,
    on_generate_query=None,
    on_copy_query=None,
    on_execute=None,
    data={},
):
    
    main(
        query=query,
        query_tool_title=query_tool_title,
        data_grid_title=data_grid_title,
        data_visualization_title=data_visualization_title,
        databases=databases,
        tables=tables,
        columns=columns,
        data=data,
        on_database_change=on_database_change,
        on_table_change=on_table_change,
        on_generate_query=on_generate_query,
        on_copy_query=on_copy_query,
        on_execute=on_execute
    )