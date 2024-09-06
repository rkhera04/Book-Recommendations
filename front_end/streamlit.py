import streamlit as st

def get_search_results(query):
    results = [
        {"title": "Result 1", "description": "Description of result 1"},
        {"title": "Result 2", "description": "Description of result 2"},
        {"title": "Result 3", "description": "Description of result 3"}
    ]
    return results

st.title("Research Paper Recommendations")

search_query = st.selectbox("Enter research paper", options=["Paper 1", "Paper 2", "Paper 3"])

col1, col2 = st.columns(2)

with col1:
    filter1 = st.selectbox("Select a filter:", options=["Content", "Author", "Year", "Publisher"])

with col2:
    if filter1 == "Author":
        filter2 = st.selectbox("Select a specific author:", options=["Author 1", "Author 2", "Author 3"])
    else:
        st.write("")

search_button = st.button("Search", use_container_width=True)

if search_button:
    if search_query:
        search_results = get_search_results(search_query)
        for result in search_results:
            st.write(f"### {result['title']}")
            st.write(f"{result['description']}")
            st.markdown("---")
    else:
        st.warning("Please enter a search query.")
