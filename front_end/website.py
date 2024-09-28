import streamlit as st
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from modeling.vectorize import score_abstracts


def get_search_results(query, df):
    sort_df = df.sort_values(by='Similarities', ascending=False)
    results = sort_df.to_dict(orient='records')
    return results

def run_streamlit(df):
    if 'page' not in st.session_state:
        st.session_state.page = 0

    if 'current_page' not in st.session_state:
        st.session_state.current_page = 1

    if 'last_search_query' not in st.session_state:
        st.session_state.last_search_query = None

    if 'search_triggered' not in st.session_state:
        st.session_state.search_triggered = False

    st.title("Research Paper Recommendations")

    st.sidebar.header("Menu")
    help_button = st.sidebar.button("Help/Info")
    update_button = st.sidebar.button("Update Data")

    if help_button:
        with st.spinner("Loading help information..."):
            st.sidebar.markdown(
                """
                ## Help & Information
                
                **Welcome to the Research Paper Recommendations app!**
                
                - **Search Query**: Select a research paper from the drop-down menu to search for related results.
                - **Filters**: Use filters to narrow down your search based on content, author, year, or publisher.
                - **Update Data**: Click the 'Update Data' button to refresh the dataset. (Note: This feature is not implemented in this example.)
                
                If you need more assistance, please contact support.
                """
            )

    if update_button:
        st.sidebar.write("Data update functionality is not implemented in this example.")

    # get titles from csv
    title_list = df['Title'].to_list()

    search_query = st.selectbox("Enter research paper", options=title_list)

    col1, col2 = st.columns(2)

    with col1:
        filter1 = st.selectbox("Select a filter:", options=["Content", "Author", "Year", "Publisher"])

    with col2:
        if filter1 == "Author":

            # get authors from csv title
            row = df[df['Title'] == search_query]
            authors_str = row['Author'].values[0]
            authors_list = [author.strip() for author in authors_str.split(',')]

            filter2 = st.selectbox("Select a specific author:", options=authors_list)
        else:
            st.write("")

    search_button = st.button("Search", use_container_width=True)

    if search_button:
        st.session_state.page = 1
        st.session_state.last_search_query = search_query
        st.session_state.search_triggered = True

    if st.session_state.page == 1 and st.session_state.last_search_query:
        papers_per_page = 10


        if st.session_state.search_triggered:
            score_abstracts(st.session_state.last_search_query, df['Abstract'], df)
            st.session_state.search_triggered = False  # Reset the flag after running

        # Updates csv with scores based on search_query
        # score_abstracts(search_query, df['Abstract'], df)
        search_results = get_search_results(search_query, df)
        total_papers = len(search_results)
        total_pages = (total_papers + papers_per_page - 1) // papers_per_page

        # Ensure current page is within range
        st.session_state.current_page = min(max(st.session_state.current_page, 1), total_pages)

        col1, col2, col3 = st.columns([1, 5, 1])

        with col1:
            if st.button("Previous"):
                if st.session_state.current_page > 1:
                    st.session_state.current_page -= 1

        with col2:
            page_number = st.selectbox(
                "Select Page",
                options=list(range(1, total_pages + 1)),
                index=st.session_state.current_page - 1
            )
            st.session_state.current_page = page_number

        with col3:
            if st.button("Next"):
                if st.session_state.current_page < total_pages:
                    st.session_state.current_page += 1

        start_index = (st.session_state.current_page - 1) * papers_per_page
        end_index = start_index + papers_per_page

        page_results = search_results[start_index:end_index]

        if page_results:
            for result in page_results:
                st.write(f"### {result['Title']}")
                st.write(f"**Author(s):** {result['Author']}")
                st.write(f"**Abstract:** {result['Abstract']}")
                st.write(f"**Year:** {result['Year']}")
                st.write(f"**Journal/Conference Name:** {result['Journal/Conference Name']}")
                st.write(f"**Conference or Journal:** {result['Conference or Journal']}")
                st.write(f"**Publisher:** {result['Publisher']}")
                st.markdown("---")
        else:
            st.warning("No data found.")