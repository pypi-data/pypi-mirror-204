import os
import streamlit.components.v1 as components

_RELEASE = True

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        "st_dropfill_textarea",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/dist")
    _component_func = components.declare_component(
        "st_dropfill_textarea", path=build_dir)

# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.


def st_dropfill_textarea(label, value,
                         placeholder="",
                         layout="column",
                         labelWidth=None,
                         height=200,
                         key=None):
    component_value = _component_func(
        label=label,
        value=value,
        labelWidth=labelWidth,
        placeholder=placeholder,
        layout=layout,
        height=height,
        key=key,
        default=value)
    return component_value


if not _RELEASE:
    import streamlit as st
    st.subheader("Component with column layout (default)")
    label = 'column layout: '
    text = ''
    returnText = st_dropfill_textarea(label, text,
                                      placeholder="Type at here",
                                      height=200)
    st.write(f"Returned text: {returnText}")

    st.subheader("Component with row layout")
    label = 'short row: '
    text_short = ''
    text_short = st_dropfill_textarea(label, text_short,
                                      placeholder="",
                                      layout="row",
                                      labelWidth=120,
                                      height=200)
    label = 'looooong row:'
    text_long = ''
    text_long = st_dropfill_textarea(label, text_long,
                                     layout="row",
                                     labelWidth=120,
                                     height=200)
    text_default = ""
    text_default = st.text_area("streamlit textarea", text_default, height=200)
    st.write(f"Returned short row: {text_short}")
    st.write(f"Returned long row: {text_long}")
    st.write(f"Returned streamlit textarea: {text_default}")
