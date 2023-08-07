# streamlit-component-dropfilltextarea

Streamlit Component DropFillTextarea allows you to drag and drop files onto a text area, making it easy to fill in large amounts of text quickly. With dropfill_textarea, users can quickly populate text areas with pre-existing text files, reducing manual input and increasing efficiency. The component also offers flexible layout options, allowing users to customize the label and text area's size, position, and other properties. Whether you're a developer or a user, dropfill_textarea is the perfect solution for simplifying your workflow.

## Installation instructions

```sh
pip install streamlit-component-dropfilltextarea
```

## Usage instructions

### Use like default textarea

```python
import streamlit as st

from st_dropfill_textarea import st_dropfill_textarea

value = st_dropfill_textarea("Your label", "")

st.write(value)

```

### Use with layout column (default) or row

```python
st.subheader("Component with column layout (default)")
returnText = st_dropfill_textarea('column layout: ', '',
                                    placeholder="Type at here",
                                    height=200)
st.write(f"Returned text: {returnText}")

st.subheader("Component with row layout")
returnText = st_dropfill_textarea('row layout: ', '',
                                    layout="row",
                                    height=200)
st.write(f"Returned text: {returnText}")

```

### Align multi rows of textarea

```python
labelWidth = 120
label = 'short row: '
text_short = ''
text_short = st_dropfill_textarea(label, text_short,
                                    placeholder="",
                                    layout="row",
                                    labelWidth=labelWidth,
                                    height=200)
label = 'looooong row:'
text_long = ''
text_long = st_dropfill_textarea(label, text_long,
                                    layout="row",
                                    labelWidth=labelWidth,
                                    height=200)


```
