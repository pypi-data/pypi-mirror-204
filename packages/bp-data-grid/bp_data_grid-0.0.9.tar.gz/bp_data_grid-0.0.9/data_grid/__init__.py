import os
from typing import List
import streamlit.components.v1 as components
import streamlit as st
from data_grid.register import (
    init,
    register_callback,
    get_component_rerender_count,
    set_component_rerender_count,
)

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = True

# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
init()

if _RELEASE:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/dist")
    __data_grid_component_function = components.declare_component(
        "data_grid", path=build_dir
    )
else:
    __data_grid_component_function = components.declare_component(
        "data_grid", url="http://localhost:4001"
    )


def __data_grid(
    rows=[],
    columns=[],
    title="",
    on_click=None,
    key="b-data-grid",
    args: tuple = (),
):
    register_callback(key, on_click, *args)
    render_count = get_component_rerender_count(key)
    data_grid_value = __data_grid_component_function(
        key=key,
        rows=rows,
        columns=columns,
        title=title,
        render_count=render_count,
    )
    set_component_rerender_count(key)
    return data_grid_value


def handle_datagrid_change(
    widget_key,
):
    response = st.session_state.get(widget_key)

def data_grid(
    key: str = "data-grid",
    rows: List = [],
    columns: List = [],
    title: str = ""
    
):
    return __data_grid(
        rows=rows,
        columns=columns,
        title=title,
        key=key,
        on_click=handle_datagrid_change,
        args=(
            key,
        ),
    )
