import streamlit as st

list = ['Email', 'Phone']
option = st.selectbox(
    "Select a research paper", list,
)

col1, col2 = st.columns(2)

with st.container(border=True):
    with col1:
        option = st.selectbox(
            "Filter", list,
        )

    with col2:
        if st.button("Search", use_container_width=True):
            row1 = st.columns(3)
            row2 = st.columns(3)

            for col in row1 + row2:
                tile = col.container(height=120)
                tile.title(":balloon:")